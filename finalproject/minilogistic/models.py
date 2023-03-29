from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from datetime import datetime, date




class User(AbstractUser):
    
    groups = models.ManyToManyField(Group, related_name='minilogistic_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='minilogistic_users', blank=True)


    def __str__(self):
        return f"{self.username}"


class Location(models.Model):
    name = models.CharField(max_length=64)
    

    def __str__(self):
        return f"{self.name}"


class Cleaner(models.Model):
    name = models.CharField(max_length=64)
    title = models.TextField(null=True, max_length=200)

    
    def __str__(self):
        return f"{self.name}"


class Booking(models.Model):
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="bookings")
    arrival_time = models.TimeField()
    arrival_date = models.DateField()
    departure_date = models.DateField()
    self_check_in = models.BooleanField(default=True)


    def __str__(self):
        return f"name:{self.firstname} {self.lastname} Location: {self.location} Arrival: {self.arrival_date}"


class Contractor(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=200)


    def __str__(self):
        return f"Contractor:{self.name}"
    
class Clean(models.Model):
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="cleans")
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.DecimalField(default=0.0, max_digits=3, decimal_places=2)
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT, related_name="cleans")
    cleaners = models.ManyToManyField(Cleaner, related_name="cleans")
    date_created = models.DateTimeField(default= datetime.today)

    def __str__(self):
        return f"Clean: {self.location} on {self.date}"
    

class Selector(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="selectors")
    agenda_date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.agenda_date}"
