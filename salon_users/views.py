from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, Reviews, Service, ServiceCategory, UserProfile
from salon_staff.models import Booking, Staff
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.http import JsonResponse
from .utils import send_otp
from datetime import datetime, timedelta
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
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validate email and password presence
        if not username or not password:
            messages.error(request, 'Phone and password are required.')
            return render(request, 'user_templates/login.html')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'No user found with this number!')
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

def request_otp(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        otp = send_otp(phone)
        
        if otp:
            request.session["otp"] = otp  # Store OTP in session
            request.session["phone"] = phone
            return redirect("verify_otp")  # Redirect to OTP verification page
        else:
            messages.error(request, "Failed to send OTP. Try again.")
    return render(request, 'user_templates/request_otp.html')

def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        session_otp = request.session.get("otp")
        phone = request.session.get("phone")

        if str(entered_otp) == str(session_otp):
            user, created = User.objects.get_or_create(username=phone)

            # If user is new, redirect to profile completion page
            if created:
                user_profile = UserProfile.objects.create(user=user)
                messages.info(request, "Please complete your profile.")
                login(request, user)
                return redirect("complete_profile")

            # If user already exists, log them in
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('/')  # Redirect to homepage

        else:
            messages.error(request, "Invalid OTP. Try again.")
    return render(request, 'user_templates/verify_otp.html')

def complete_profile(request):
    """Page where new users enter their details after OTP verification."""
    genders = UserProfile.GENDER_CHOICES
    if request.method == "POST":
        user_obj = request.user

        user_obj.first_name = request.POST.get("first_name", "")
        user_obj.last_name = request.POST.get("last_name", "")

        user_profile, created = UserProfile.objects.get_or_create(user=user_obj)

        user_profile.phone = user_obj.username
        user_profile.gender = request.POST.get("gender", "")
        user_profile.age = request.POST.get("age", None)

        email = request.POST.get("email", "").strip()
        if email:  # Store email only if provided
            user_obj.email = email

        user_obj.save()
        user_profile.save()

        messages.success(request, "Profile completed successfully!")
        return redirect("/")  # Redirect to homepage

    return render(request, 'user_templates/complete_profile.html', {'genders': genders})

def logout_view(request):
    logout(request)
    return redirect('/')  

def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country_code = request.POST.get('country')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        dob = request.POST.get('dob', '')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=phone).exists():
            messages.error(request, "You already have an active account.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('register')
        
        if name:
            name_parts = name.split()
            first_name = name_parts[0]  # First word as first_name
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""  # Rest as last_name
        else:
            first_name = ""
            last_name = ""

        # Create User
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=phone,
            email=email,
            password=make_password(password)  # Hash the password for security
        )
        
        profile = UserProfile.objects.create(
            user=user,
            phone=phone,
            country_code=country_code,
            gender=gender if gender else None,
            age=age if age else None,
            dob=dob if dob else None
        )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')
    genders = UserProfile.GENDER_CHOICES 

    return render(request, 'user_templates/register.html', {'genders': genders})


@login_required(login_url='login')
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
        
        user = get_object_or_404(UserProfile, user=request.user)
        if not user:
            messages.error(request, 'User not found!')
        
        # Convert date and time to datetime objects
        start_time = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M').time()
        end_time = (datetime.combine(datetime.min, start_time) + timedelta(minutes=service.duration)).time()


        # Check for overlapping bookings
        conflicting_bookings = Booking.objects.filter(
            staff=staff,
            date=date,
            start_time__lt=end_time,  # New booking starts before an existing one ends
            end_time__gt=start_time,  # New booking ends after an existing one starts
            status="confirmed"
        )

        if conflicting_bookings.exists():
            messages.error(request, "The selected staff is not available at this time.")
            return redirect('book_service')

        # Save the booking
        # customer = UserProfile.objects.filter(user=user).first()

        # Save the booking
        booking = Booking.objects.create(
            customer=user,
            staff=staff if staff_id else None,
            service=service,
            date=date,
            start_time=time,
            status='Confirmed'
        )

        messages.success(request, 'Booking created successfully! Please wait for confirmation.')
        return redirect('booking_history')

    return render(request, 'user_templates/book_service.html', {'categories': categories, 'services': services, 'staffs': staffs})

def get_services_by_category(request):
    category_id = request.GET.get('category_id')
    if category_id:
        services = Service.objects.filter(category__id=category_id, is_active=True).values('id', 'name')
        return JsonResponse({"services": list(services)}, safe=False)
    return JsonResponse({"services": []}, safe=False)

def get_staff_by_services(request):
    service_id = request.GET.get('service_id')
    if service_id:
        service = get_object_or_404(Service, id=service_id)

        staffs = service.staff_members.all()
        staff_data = [{"id": staff.id, "name": staff.user.get_full_name()} for staff in staffs]

        return JsonResponse({"staffs": staff_data}, safe=False)
        
    return JsonResponse({"staffs": []}, safe=False)

@login_required(login_url='login')
def booking_history(request):
    bookings = Booking.objects.filter(customer__user=request.user)
    paginator = Paginator(bookings, 5)  # Show 10 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user_templates/booking_history.html', {'page_obj': page_obj, 'bookings': bookings})

@login_required(login_url='login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer__user=request.user)

    if booking.status == 'canceled':
        messages.error(request, 'This booking is already canceled.')
    else:
        booking.status = 'canceled'
        booking.save()
        messages.success(request, 'Booking canceled successfully.')

    return redirect('booking_history')

@login_required(login_url='login')
def my_profile(request):    
    user = request.user
    user_profile = UserProfile.objects.filter(user=user).first()
    return render(request, 'user_templates/my_profile.html', {'user_profile':user_profile})

@login_required(login_url='login')
def edit_profile(request):
    if request.POST:
        return None
    return render(request, 'user_templates/edit_profile.html')
    