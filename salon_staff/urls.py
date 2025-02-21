from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_index, name='admin_index'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('admin_login/', views.admin_login, name='admin_login'),
    
    path('admin_all_bookings/', views.admin_all_bookings, name='admin_all_bookings'),
    path('admin_del_booking/<int:id>/', views.admin_del_booking, name='admin_del_booking'),
    path('admin_edit_booking/<int:id>/', views.admin_edit_booking, name='admin_edit_booking'),
    path('admin_add_booking/', views.admin_add_booking, name='admin_add_booking'),


    # CRUD for staff profiles.
    path('admin_staff_profiles/', views.admin_staff_profiles, name='admin_staff_profiles'),
    path('admin_del_staff/<int:id>/', views.admin_del_staff, name='admin_del_staff'),
    path('admin_edit_staff/<int:id>/', views.admin_edit_staff, name='admin_edit_staff'),
    path('admin_add_staff/', views.admin_add_staff, name='admin_add_staff'),

    # CRUD for service categories.
    path('admin_service_categories/', views.admin_service_categories, name='admin_service_categories'),
    path('admin_del_service_category/<int:id>/', views.admin_del_service_category, name='admin_del_service_category'),
    path('admin_edit_service_category/<int:id>/', views.admin_edit_service_category, name='admin_edit_service_category'),
    path('admin_add_service_category/', views.admin_add_service_category, name='admin_add_service_category'),

    # CRUD for services.
    path('admin_services/', views.admin_services, name='admin_services'),
    path('admin_del_service/<int:id>/', views.admin_del_service, name='admin_del_service'),
    path('admin_edit_service/<int:id>/', views.admin_edit_service, name='admin_edit_service'),
    path('admin_add_service/', views.admin_add_service, name='admin_add_service'),

    # CRUD for blogs.
    path('admin_blogs/', views.admin_blogs, name='admin_blogs'),
    path('admin_del_blog/<int:id>/', views.admin_del_blog, name='admin_del_blog'),
    path('admin_edit_blog/<int:id>/', views.admin_edit_blog, name='admin_edit_blog'),
    path('admin_add_blog/', views.admin_add_blog, name='admin_add_blog'),

    # CRUD for customers.
    path('admin_customers/', views.admin_customers, name='admin_customers'),
    path('admin_del_customer/<int:id>/', views.admin_del_customer, name='admin_del_customer'),

    # CRUD for reviews.
    path('admin_reviews/', views.admin_reviews, name='admin_reviews'),
    path('admin_del_review/<int:id>/', views.admin_del_review, name='admin_del_review'),
    path('admin_edit_review/<int:id>/', views.admin_edit_review, name='admin_edit_review'),
    path('admin_add_review/', views.admin_add_review, name='admin_add_review'),

]