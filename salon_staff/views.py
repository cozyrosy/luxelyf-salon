from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from .models import Staff, StaffAvailability, Booking

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

def admin_service_categories(request):
    return render(request, 'admin_staff_templates/admin_service_categories.html')

def admin_services(request):
    return render(request, 'admin_staff_templates/admin_services.html')

def admin_blogs(request):
    return render(request, 'admin_staff_templates/admin_blogs.html')

def admin_reviews(request):
    return render(request, 'admin_staff_templates/admin_reviews.html')

def admin_customers(request):
    return render(request, 'admin_staff_templates/admin_customers.html')