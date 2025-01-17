from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.service_categories, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact/', views.contact, name='contact'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog_detail/<int:id>/', views.blog_detail, name='blog_detail'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
