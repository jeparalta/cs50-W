from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime



class User(AbstractUser):
    pass
    watchlist =models.ManyToManyField('Listing', blank=True, related_name="users_watching")
    

    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=200)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    price = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(default=datetime.today)
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="listings")
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT, related_name="listings")
    bid_count = models.IntegerField(null=True, default=0)
    current_winner = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name="winning_bids")
    

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    bidder = models.ForeignKey(User,on_delete=models.PROTECT, related_name="user_bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bids")
    amount = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    date_added = models.DateTimeField(default=datetime.today)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Bidder:{self.bidder} Listing: {self.listing} Amount: {self.amount} Active: {self.active}"

class Comment(models.Model):
    commenter = models.ForeignKey(User,on_delete=models.PROTECT, related_name="user_comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    title = models.CharField(max_length=64)
    body = models.CharField(max_length=200)

    def __str__(self):
        return f"Comment:{self.comment} By:{self.commenter} for Listing: {self.listing}"

