from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from .models import Staff, StaffAvailability, Booking
from salon_users.models import Blog, Reviews, Service, ServiceCategory, UserProfile

# Create your views here.

def admin_index(request):
    return render(request, 'admin_staff_templates/admin_index.html')

def admin_all_bookings(request):
    all_bookings = Booking.objects.all().order_by('-created_at')
    pendings = all_bookings.filter(status='Pending')
    confirmed = all_bookings.filter(status='Confirmed')


    
    return render(request, 'admin_staff_templates/admin_all_bookings.html', {'all_bookings': all_bookings, 'pendings': pendings
        , 'confirmed': confirmed})

def admin_staff_profiles(request):
    staffs = Staff.objects.all()
    return render(request, 'admin_staff_templates/admin_staff_profile.html', {'staffs': staffs})


# CRUD for service categories.
def admin_service_categories(request):
    categories = ServiceCategory.objects.all()

    paginator = Paginator(categories, 5)  # Show 10 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_staff_templates/admin_service_categories.html', {'page_obj': page_obj})

def admin_del_service_category(request, id):
    category = get_object_or_404(ServiceCategory, id=id)
    category.delete()
    messages.success(request, 'Service category deleted successfully.')
    return redirect('admin_service_categories')

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
def admin_services(request):
    services = Service.objects.all()

    paginator = Paginator(services, 5)  # Show 10 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_staff_templates/admin_services.html', {'page_obj': page_obj})

def admin_del_service(request, id):
    service = get_object_or_404(Service, id=id)
    service.delete()
    messages.success(request, 'Service deleted successfully.')
    return redirect('admin_services')

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
def admin_blogs(request):
    blogs = Blog.objects.all().order_by('-date')

    paginator = Paginator(blogs, 5)  # Show 10 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_staff_templates/admin_blogs.html', {'page_obj': page_obj})

def admin_del_blog(request, id):
    blog = get_object_or_404(Blog, id=id)
    blog.delete()
    messages.success(request, 'Blog deleted successfully.')
    return redirect('admin_blogs')

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
def admin_reviews(request):
    reviews = Reviews.objects.all().order_by('-created_at')

    paginator = Paginator(reviews, 5)  # Show 10 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_staff_templates/admin_reviews.html', {'page_obj': page_obj})

def admin_del_review(request, id):
    review = get_object_or_404(Reviews, id=id)
    review.delete()
    messages.success(request, 'Review deleted successfully.')
    return redirect('admin_reviews')

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
def admin_customers(request):
    customers = UserProfile.objects.filter(user_role='customer')

    paginator = Paginator(customers, 5)  # Show 10 bookings per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin_staff_templates/admin_customers.html', {'page_obj': page_obj})

def admin_del_customer(request, id):
    customer = get_object_or_404(UserProfile, id=id)
    customer.delete()
    messages.success(request, 'Customer deleted successfully.')
    return redirect('admin_customers')