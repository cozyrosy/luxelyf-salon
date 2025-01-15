from django.contrib import admin
from .models import Blog, CustomerInquiry, Portfolio, Services, ServiceCategory, UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Services)
admin.site.register(Portfolio)
admin.site.register(Blog)
admin.site.register(CustomerInquiry)
admin.site.register(ServiceCategory)

