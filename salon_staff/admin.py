from django.contrib import admin
from .models import Staff, StaffAvailability, Booking

# Register your models here.
admin.site.register(Staff)
admin.site.register(StaffAvailability)
admin.site.register(Booking)

