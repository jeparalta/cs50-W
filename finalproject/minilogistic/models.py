from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from datetime import datetime, date
from enum import Enum
from phonenumber_field.modelfields import PhoneNumberField

class PermissionLevel(Enum):
    VIEW_ONLY = 'View Only'
    EDIT = 'Edit'
    ADMIN = 'Admin'

    def __str__(self):
        return self.value
    
class ColorCode(Enum):
    GREEN = 'Green'
    RED = 'Red'
    BLUE = 'Blue'

    def __str__(self):
        return self.value


class User(AbstractUser):
    
    groups = models.ManyToManyField(Group, related_name='minilogistic_users', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='minilogistic_users', blank=True)
    


    def __str__(self):
        return f"{self.username}"
    

class Account(models.Model):
    name = models.CharField(max_length=64)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts_created", blank=True)
    date_created = models.DateTimeField(default= datetime.today)

    def share_with(self, user, permission_level=PermissionLevel.VIEW_ONLY):
        account_user, created = AccountUser.objects.get_or_create(user=user, account=self)
        account_user.permission_level = permission_level
        account_user.save()
    

    def __str__(self):
        return f"{self.name}"
    
    
class AccountUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account_users')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='account_users')
    permission_level = models.CharField(max_length=20, choices=[(level, level.value) for level in PermissionLevel])

    def __str__(self):
        return f"{self.user} - {self.account} - {self.permission_level}"




class Location(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="locations")
    name = models.CharField(max_length=64)
    address = models.TextField(max_length=200, blank=True)
    comment = models.TextField(max_length=500, blank=True)
    date_created = models.DateTimeField(default= datetime.today)
    

    def __str__(self):
        return f"{self.name}"


class Cleaner(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="cleaners")
    name = models.CharField(max_length=64)
    title = models.TextField(null=True, max_length=200)
    email = models.EmailField(blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    date_created = models.DateTimeField(default= datetime.today)
    

    
    def __str__(self):
        return f"{self.name}"


class Booking(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="bookings")
    firstname = models.CharField(max_length=64)
    lastname = models.CharField(max_length=64)
    email = models.EmailField(blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="bookings")
    arrival_time = models.TimeField()
    arrival_date = models.DateField()
    departure_date = models.DateField()
    comment = models.TextField(max_length=500)
    self_check_in = models.BooleanField(default=True)
    date_created = models.DateTimeField(default= datetime.today)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings_added", blank=True)


    def __str__(self):
        return f"name:{self.firstname} {self.lastname} Location: {self.location} Arrival: {self.arrival_date}"


class Contractor(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="contractors")
    name = models.CharField(max_length=64)
    email = models.EmailField(blank=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    description = models.TextField(max_length=200)
    date_created = models.DateTimeField(default= datetime.today)


    def __str__(self):
        return f"Contractor:{self.name}"
    
    
class Clean(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="cleans")
    
    location = models.ForeignKey(Location, on_delete=models.PROTECT, related_name="cleans")
    date = models.DateField()
    start_time = models.TimeField() 
    duration = models.DecimalField(default=0.0, max_digits=3, decimal_places=2)
    arrival_time = models.TimeField(null=True)
    cleaners = models.ManyToManyField(Cleaner, related_name="cleans")
    same_day = models.BooleanField(default=False)
    comment = models.TextField(max_length=500, blank=True)
    date_created = models.DateTimeField(default= datetime.today)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cleans_added", blank=True)

    def __str__(self):
        return f"Clean: {self.location} on {self.date}"

class Comment(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    clean = models.ForeignKey(Clean, on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    date_created = models.DateTimeField(default= datetime.today)
    active = models.BooleanField(default=True)
    color = models.CharField(max_length=20, choices=[(color, color.value) for color in ColorCode])
    
    body = models.TextField(null=True, max_length=200)
    
    
    

    
    def __str__(self):
        return f"{self.id}"
    

class Selector(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="selectors")
    agenda_date = models.DateField(default=date.today)
    agenda_horizontal = models.BooleanField(default=False)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, related_name="selected_account", blank=True)

    def __str__(self):
        return f"{self.user}"
