from django.shortcuts import render, redirect, get_object_or_404
from .models import Blog, ServiceCategory

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
    