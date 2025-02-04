from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Reviews, Service, ServiceCategory, UserProfile
from salon_staff.models import Booking, Staff
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.http import JsonResponse
# Create your views here.

def index(request):
    service_cat = ServiceCategory.objects.filter(is_active=True, add_to_home=True)
    blogs = Blog.objects.all()
    team = Staff.objects.filter(is_active=True)
    reviews = Reviews.objects.filter(add_to_home=True).order_by('-created_at')[:10]
    services = Service.objects.filter(is_active=True, add_to_home=True)

    return render(request, 'index.html', {
        'service_cat': service_cat, 'blogs':blogs, 
        'team':team, 'reviews':reviews, 'services':services
        })

def about(request):
    team = Staff.objects.filter(is_active=True)

    return render(request, 'about.html', {'team': team})

def service_categories(request):
    services = ServiceCategory.objects.filter(is_active=True)
    return render(request, 'services.html', {'services': services})

def portfolio(request):
    return render(request, 'portfolio.html')

def contact(request):
    return render(request, 'contact.html')

def blogs(request):
    blogs = Blog.objects.all().order_by('-date')

    paginator = Paginator(blogs, 4)  # Show 4 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blogs.html', context={'page_obj': page_obj})

def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'blog_detail.html', {'blog': blog})
    

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate email and password presence
        if not email or not password:
            messages.error(request, 'Email and password are required.')
            return render(request, 'user_templates/login.html')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user found with this email!')
            return render(request, 'user_templates/login.html')

        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'This account is inactive.')
                return render(request, 'user_templates/login.html')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'user_templates/login.html')
    return render(request, 'user_templates/login.html')

def logout_view(request):
    logout(request)
    return redirect('/')  

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username', '')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country_code = request.POST.get('country')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')

        # Create User
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)  # Hash the password for security
        )
        
        profile = UserProfile.objects.create(
            user=user,
            phone=phone,
            country_code=country_code,
            gender=gender if gender else None,
            age=age if age else None
        )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')
    genders = UserProfile.GENDER_CHOICES 

    return render(request, 'user_templates/register.html', {'genders': genders})



def book_service(request):
    categories = ServiceCategory.objects.filter(is_active=True)
    services = Service.objects.filter(is_active=True)
    staffs = Staff.objects.filter(is_active=True)   

    if request.method == 'POST':
        category_id = request.POST.get('category')
        service_id = request.POST.get('service')
        staff_id = request.POST.get('staff', None)
        date = request.POST.get('date')
        time = request.POST.get('time')

        # Validate inputs
        if not service_id or not category_id or not date or not time:
            messages.error(request, 'Please fill all the required fields.')
            return redirect('book_service')

        service = get_object_or_404(Service, id=service_id)
        if not service:
            messages.error(request, 'Invalid service selected.')

        if staff_id:
            staff = Staff.objects.filter(id=staff_id).first()
            if not staff:
                messages.error(request, 'Invalid staff selected.')

        # Convert date and time to datetime objects
        start_time = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
        end_time = start_time + timedelta(hours=1)

        # Check if the staff is available during the selected time
        conflicting_bookings = Booking.objects.filter(
            staff_id=staff_id,
            date=date,
            status='confirmed',
            time=time,
        )

        if conflicting_bookings.exists():
            messages.error(request, 'The selected staff is not available at the chosen time.')
            return redirect('book_service')

        # Save the booking
        service = get_object_or_404(Service, id=service_id)
        user = get_object_or_404(User, id=request.user.id)
        customer = UserProfile.objects.filter(user=user).first()

        # Save the booking
        booking = Booking.objects.create(
            customer=customer,
            staff=staff if staff_id else None,
            service=service,
            date=date,
            time=time,
            status='Pending'
        )

        messages.success(request, 'Booking created successfully! Please wait for confirmation.')
        return redirect('booking_history')

    return render(request, 'user_templates/book_service.html', {'categories': categories, 'services': services, 'staffs': staffs})

def get_services_by_category(request, category_id):
    services = Service.objects.filter(category__id=category_id, is_active=True)
    services_list = list(services.values('id', 'name'))
    return JsonResponse(services_list, safe=False)

def booking_history(request):
    bookings = Booking.objects.filter(customer__user=request.user)
    paginator = Paginator(bookings, 5)  # Show 10 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user_templates/booking_history.html', {'page_obj': page_obj, 'bookings': bookings})

def my_profile(request):    
    return render(request, 'user_templates/my_profile.html')
    