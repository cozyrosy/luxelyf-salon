from django.contrib import admin
from .models import UserProfile, Services, Portfolio, Blog, CustomerInquiry

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Services)
admin.site.register(Portfolio)
admin.site.register(Blog)
admin.site.register(CustomerInquiry)

