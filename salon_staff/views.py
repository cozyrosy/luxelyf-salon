from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from .models import Staff, StaffAvailability, Booking

# Create your views here.

def admin_index(request):
    return render(request, 'admin_templates/admin_index.html')

def admin_all_bookings(request):
    all_bookings = Booking.objects.all().order_by('-created_at')
    pendings = all_bookings.filter(status='Pending')
    confirmed = all_bookings.filter(status='Confirmed')


    
    return render(request, 'admin_templates/admin_all_bookings.html', {'all_bookings': all_bookings, 'pendings': pendings
        , 'confirmed': confirmed})