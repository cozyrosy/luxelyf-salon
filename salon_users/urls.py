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

    path('login/', views.login_view, name='login'),
     path("login_with_otp/", views.request_otp, name="login_with_otp"),
    path("verify_otp/", views.verify_otp, name="verify_otp"),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    path('book_service/', views.book_service, name='book_service'),
    path('get_services_by_category/<int:id>/', views.get_services_by_category, name='get_services_by_category'),
    path('booking_history/', views.booking_history, name='booking_history'),
    path('my_profile/', views.my_profile, name='my_profile'),
]