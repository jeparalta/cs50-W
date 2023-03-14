from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    
    followers = models.ManyToManyField('self', symmetrical=False, blank=True, related_name="following")

    def __str__(self):
        return f"{self.username}"
    

class Post(models.Model):
    poster = models.ForeignKey(User,on_delete=models.PROTECT, related_name="user_posts")
    body = models.TextField(max_length=300)
    liked_by = models.ManyToManyField(User, blank=True, related_name='liked_posts')
    timestamp = models.DateTimeField(default=datetime.today)

    def __str__(self):
        return f"Post by: {self.poster} On: {self.timestamp}"
    

class Comment(models.Model):
    commenter = models.ForeignKey(User,on_delete=models.PROTECT, related_name="user_comments")
    Post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="listing_comments")
    body = models.CharField(max_length=200)

    def __str__(self):
        return f"Comment:{self.comment} By:{self.commenter} for Listing: {self.listing}"
