from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from salon_users.models import TimestampedModel, Service, UserProfile

# Create your models here.

class Staff(UserProfile):
    role = models.CharField(max_length=255)
    services = models.ManyToManyField(Service, related_name="staff_members") 

    def __str__(self):
        return self.user.get_full_name()


class StaffAvailability(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='availability')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('staff', 'date', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.staff.user.get_full_name()} - {self.date} ({self.start_time} to {self.end_time})"


class Booking(TimestampedModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, related_name='staff')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)  
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def save(self, *args, **kwargs):
        """
        Automatically calculates end_time before saving.
        """
        from datetime import datetime, timedelta
        if self.start_time and self.service:
            # Ensure self.start_time is a time object
            if isinstance(self.start_time, str):
                self.start_time = datetime.strptime(self.start_time, "%H:%M").time()  # Convert string to time

                # Calculate end_time correctly
                self.end_time = (datetime.combine(datetime.min, self.start_time) + timedelta(minutes=self.service.duration)).time()

        super().save(*args, **kwargs)  # Call the original save() method

    def __str__(self):
        return f"Booking by {self.customer.user.username} for {self.service.name} on {self.date} at {self.start_time}"