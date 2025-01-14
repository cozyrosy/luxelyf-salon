from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey( User, related_name='created_%(class)s_set', on_delete=models.SET_NULL, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey( User, related_name='updated_%(class)s_set', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class Services(TimestampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')
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
