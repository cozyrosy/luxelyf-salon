from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_index, name='admin_index'),
    path('admin_all_bookings/', views.admin_all_bookings, name='admin_all_bookings'),
]