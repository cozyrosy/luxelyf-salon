from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from .models import Staff, StaffAvailability, Booking
from salon_users.models import Blog, Reviews, Service, ServiceCategory, UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore as session


# Create your views here.

@login_required(login_url='admin_login')
def admin_index(request):
    if request.user.is_authenticated:
        return render(request, 'admin_staff_templates/admin_index.html')
    


# Admin authentication
def admin_logout(request):
    logout(request)
    request.session.flush()
    return redirect('admin_login')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # import pdb; pdb.set_trace()
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('admin_index')
            else:
                messages.error(request, 'You are not authorized to access this page.')
                return redirect('admin_login')
        else:
            messages.error(request, 'Invalid credentials.')
            return redirect('admin_login')
    else:
        return render(request, 'admin_staff_templates/admin_login.html')


# CRUD for bookings.
@login_required(login_url='admin_login')
def admin_all_bookings(request):
    all_bookings = Booking.objects.all().order_by('-created_at')
    services = Service.objects.filter(is_active=True)
    staffs = Staff.objects.filter(user_role='staff', is_active=True)
    customers = UserProfile.objects.filter(user_role='customer', is_active=True)
    
    
    return render(request, 'admin_staff_templates/admin_all_bookings.html', {
        'all_bookings': all_bookings, 'services': services, 'staffs': staffs, 
        'customers': customers, 'booking_status_choices': Booking.STATUS_CHOICES
        })

@login_required(login_url='admin_login')
def admin_del_booking(request, id):
    booking = get_object_or_404(Booking, id=id)
    booking.delete()
    messages.success(request, 'Booking deleted successfully.')
    return redirect('admin_all_bookings')

@login_required(login_url='admin_login')
def admin_edit_booking(request, id):
    if request.method == 'POST':
        booking = get_object_or_404(Booking, id=id)
        booking.customer = get_object_or_404(UserProfile, id=request.POST['customer'])
        booking.service = get_object_or_404(Service, id=request.POST['service'])
        booking.staff = get_object_or_404(Staff, id=request.POST['staff'])
        booking.date = request.POST['date']
        booking.start_time = request.POST['time']
        booking.status = request.POST['status']
        booking.save()
        messages.success(request, 'Booking updated successfully.')
        return redirect('admin_all_bookings')
    else:
        booking = get_object_or_404(Booking, id=id)
        return redirect('admin_all_bookings')

@login_required(login_url='admin_login')
def admin_add_booking(request):
    if request.method == 'POST':
        booking = Booking()
        booking.customer = get_object_or_404(UserProfile, id=request.POST['customer'])
        booking.service = get_object_or_404(Service, id=request.POST['service'])
        booking.staff = get_object_or_404(Staff, id=request.POST['staff'])
        booking.date = request.POST['date']
        booking.start_time = request.POST['time']
        booking.status = request.POST['status']
        booking.save()
        messages.success(request, 'Booking added successfully.')
        return redirect('admin_all_bookings')
    else:
        return redirect('admin_all_bookings')


# CRUD for staff profiles.
@login_required(login_url='admin_login')
def admin_staff_profiles(request):
    staffs = Staff.objects.all()
    return render(request, 'admin_staff_templates/admin_staff_profile.html', {'staffs': staffs})

@login_required(login_url='admin_login')
def admin_del_staff(request, id):
    staff = get_object_or_404(Staff, id=id)
    staff.delete()
    messages.success(request, 'Staff deleted successfully.')
    return redirect('admin_staff_profiles')

@login_required(login_url='admin_login')
def admin_edit_staff(request, id):
    if request.method == 'POST':
        staff = get_object_or_404(Staff, id=id)
        user_name = request.POST.get('user_name', '')
        email = request.POST['email']

        if user_name != staff.user.username:
            staff.user.username = user_name
        if email != staff.user.email:
            staff.user.email = email

        staff.user.first_name = request.POST['first_name']
        staff.user.last_name = request.POST['last_name']
        staff.user.save()

        staff.country_code = request.POST['country_code']
        staff.phone = request.POST['phone']
        staff.address = request.POST['address']
        staff.image = request.FILES['image']
        staff.save()
        messages.success(request, 'Staff updated successfully.')
        return redirect('admin_staff_profiles')
    else:
        staff = get_object_or_404(Staff, id=id)
        return redirect('admin_staff_profiles')

@login_required(login_url='admin_login')
def admin_add_staff(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('admin_staff_profiles')

        user = User.objects.create_user(
            username=request.POST.get('username', ''), 
            email=request.POST['email'], 
            password=request.POST['password']
            )
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()

        staff = Staff()
        staff.user = user
        staff.country_code = request.POST['country_code']
        staff.phone = request.POST['phone']
        staff.address = request.POST['address']
        staff.image = request.FILES['image']

        staff.save()
        messages.success(request, 'Staff added successfully.')
        return redirect('admin_staff_profiles')
    else:
        return redirect('admin_staff_profiles')


# CRUD for service categories.
@login_required(login_url='admin_login')
def admin_service_categories(request):
    categories = ServiceCategory.objects.all()

    paginator = Paginator(categories, 5)  # Show 10 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_staff_templates/admin_service_categories.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
def admin_del_service_category(request, id):
    category = get_object_or_404(ServiceCategory, id=id)
    category.delete()
    messages.success(request, 'Service category deleted successfully.')
    return redirect('admin_service_categories')

@login_required(login_url='admin_login')
def admin_edit_service_category(request, id):
    if request.method == 'POST':
        category = get_object_or_404(ServiceCategory, id=id)
        category.name = request.POST['name']
        category.description = request.POST['description']
        category.add_to_home = 'add_to_home' in request.POST
        category.is_active = 'is_active' in request.POST
        if 'image' in request.FILES:
            category.image = request.FILES['image']
        else:
            category.image = category.image
        category.save()
        messages.success(request, 'Service category updated successfully.')
        return redirect('admin_service_categories')
    else:
        category = get_object_or_404(ServiceCategory, id=id)
        return redirect('admin_service_categories')

@login_required(login_url='admin_login')
def admin_add_service_category(request):
    if request.method == 'POST':
        category = ServiceCategory()
        category.name = request.POST['name']
        category.description = request.POST['description']
        category.add_to_home = 'add_to_home' in request.POST
        category.is_active = 'is_active' in request.POST
        category.image = request.FILES['image']
        category.save()
        messages.success(request, 'Service category added successfully.')
        return redirect('admin_service_categories')
    else:
        return redirect('admin_service_categories')


# CRUD for services.
@login_required(login_url='admin_login')
def admin_services(request):
    services = Service.objects.all()

    paginator = Paginator(services, 5)  # Show 10 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_staff_templates/admin_services.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
def admin_del_service(request, id):
    service = get_object_or_404(Service, id=id)
    service.delete()
    messages.success(request, 'Service deleted successfully.')
    return redirect('admin_services')

@login_required(login_url='admin_login')
def admin_edit_service(request, id):
    if request.method == 'POST':
        service = get_object_or_404(Service, id=id)
        service.name = request.POST['name']
        service.description = request.POST['description']
        service.add_to_home = 'add_to_home' in request.POST
        service.is_active = 'is_active' in request.POST
        if 'image' in request.FILES:
            service.image = request.FILES['image']
        else:
            service.image = service.image
        service.save()
        messages.success(request, 'Service updated successfully.')
        return redirect('admin_services')
    else:
        service = get_object_or_404(Service, id=id)
        return redirect('admin_services')

@login_required(login_url='admin_login')
def admin_add_service(request):
    if request.method == 'POST':
        service = Service()
        service.name = request.POST['name']
        service.description = request.POST['description']
        service.add_to_home = 'add_to_home' in request.POST
        service.is_active = 'is_active' in request.POST
        service.image = request.FILES['image']
        service.save()
        messages.success(request, 'Service added successfully.')
        return redirect('admin_services')
    else:
        return redirect('admin_services')


# CRUD for blogs.
@login_required(login_url='admin_login')
def admin_blogs(request):
    blogs = Blog.objects.all().order_by('-date')

    paginator = Paginator(blogs, 5)  # Show 10 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_staff_templates/admin_blogs.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
def admin_del_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    blog.delete()
    messages.success(request, 'Blog deleted successfully.')
    return redirect('admin_blogs')

@login_required(login_url='admin_login')
def admin_edit_blog(request, id):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, id=id)
        blog.title = request.POST['title']
        blog.description = request.POST['description']
        blog.author = request.POST['author']
        blog.date = request.POST['date']
        if 'image' in request.FILES:
            blog.image = request.FILES['image']
        else:
            blog.image = blog.image
        blog.save()
        messages.success(request, 'Blog updated successfully.')
        return redirect('admin_blogs')
    else:
        blog = get_object_or_404(Blog, id=id)
        return redirect('admin_blogs')

@login_required(login_url='admin_login')
def admin_add_blog(request):
    if request.method == 'POST':
        blog = Blog()
        blog.title = request.POST['title']
        blog.description = request.POST['description']
        blog.author = request.POST['author']
        blog.date = request.POST['date']
        blog.image = request.FILES['image']
        blog.save()
        messages.success(request, 'Blog added successfully.')
        return redirect('admin_blogs')
    else:
        return redirect('admin_blogs')


# CRUD for reviews.
@login_required(login_url='admin_login')
def admin_reviews(request):
    reviews = Reviews.objects.all().order_by('-created_at')

    paginator = Paginator(reviews, 5)  # Show 10 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_staff_templates/admin_reviews.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
def admin_del_review(request, id):
    review = get_object_or_404(Reviews, id=id)
    review.delete()
    messages.success(request, 'Review deleted successfully.')
    return redirect('admin_reviews')

@login_required(login_url='admin_login')
def admin_edit_review(request, id):
    if request.method == 'POST':
        review = get_object_or_404(Reviews, id=id)
        review.review = request.POST['review']
        review.author = request.POST['author']
        review.add_to_home = 'add_to_home' in request.POST
        review.save()
        messages.success(request, 'Review updated successfully.')
        return redirect('admin_reviews')
    else:
        review = get_object_or_404(Reviews, id=id)
        return redirect('admin_reviews')

@login_required(login_url='admin_login')
def admin_add_review(request):
    if request.method == 'POST':
        review = Reviews()
        review.review = request.POST['review']
        review.author = request.POST['author']
        review.add_to_home = 'add_to_home' in request.POST
        review.save()
        messages.success(request, 'Review added successfully.')
        return redirect('admin_reviews')
    else:
        return redirect('admin_reviews')


# CRUD for customers.
@login_required(login_url='admin_login')
def admin_customers(request):
    customers = UserProfile.objects.filter(user_role='customer')

    paginator = Paginator(customers, 5)  # Show 10 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_staff_templates/admin_customers.html', {'page_obj': page_obj})

@login_required(login_url='admin_login')
def admin_del_customer(request, id):
    customer = get_object_or_404(UserProfile, id=id)
    customer.delete()
    messages.success(request, 'Customer deleted successfully.')
    return redirect('admin_customers')