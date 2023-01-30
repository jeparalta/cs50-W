from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=200)
    price = models.FloatField()
    date_added = models.DateTimeField(default=datetime.today)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="listings")

    def __str__(self):
        return f"{self.title}"


