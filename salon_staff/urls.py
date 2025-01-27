from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_index, name='admin_index'),
    path('admin_all_bookings/', views.admin_all_bookings, name='admin_all_bookings'),
    path('admin_staff_profiles/', views.admin_staff_profiles, name='admin_staff_profiles'),
    path('admin_service_categories/', views.admin_service_categories, name='admin_service_categories'),
    path('admin_services/', views.admin_services, name='admin_services'),
    path('admin_blogs/', views.admin_blogs, name='admin_blogs'),
    path('admin_customers/', views.admin_customers, name='admin_customers'),
    path('admin_reviews/', views.admin_reviews, name='admin_reviews'),

]