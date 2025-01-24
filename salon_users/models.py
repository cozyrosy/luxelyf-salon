from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country_code = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='static/profiles/', blank=True, null=True)
    gender = models.CharField(max_length=10, choices=(('other', 'Other'), ('male', 'Male'), ('female', 'Female')), default='other', blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey( User, related_name='created_%(class)s_set', on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey( User, related_name='updated_%(class)s_set', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class ServiceCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='service_categories/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    add_to_home = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='static/services/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Portfolio(TimestampedModel):
    image = models.ImageField(upload_to='portfolio/')

    def __str__(self):
        return f"Portfolio Image {self.id}"


class Blog(TimestampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blogs/')
    date = models.DateField()

    def __str__(self):
        return self.title


class CustomerInquiry(TimestampedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    country_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    subject = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.subject}"
