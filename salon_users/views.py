from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, ServiceCategory, UserProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
# Create your views here.

def index(request):
    services = ServiceCategory.objects.filter(is_active=True, add_to_home=True)
    blogs = Blog.objects.all()
    return render(request, 'index.html', {'services': services, 'blogs':blogs})

def about(request):
    return render(request, 'about.html')

def service_categories(request):
    services = ServiceCategory.objects.filter(is_active=True)
    return render(request, 'services.html', {'services': services})

def portfolio(request):
    return render(request, 'portfolio.html')

def contact(request):
    return render(request, 'contact.html')

def blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'blogs.html', context={'blogs': blogs})

def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)
    return render(request, 'blog_detail.html', {'blog': blog})
    

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/') 
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('/')  

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        # country_code = request.POST.get('country_code')
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
            # country_code=country_code,
            gender=gender,
            age=age
        )

        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'register.html')
