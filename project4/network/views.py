from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, Post, Comment


"""FORMS"""
class NewPostform(forms.Form):
    body = forms.CharField(label="", widget=forms.Textarea(attrs={"rows":"5", "class": "form-control"}))
    


def index(request):

    if request.method == "POST":
        form = NewPostform(request.POST)
        if form.is_valid:
            newpost = Post(poster = request.user, body = request.POST["body"])
            newpost.save()
        return HttpResponseRedirect(reverse("network:index"))

    else:
        posts = Post.objects.all().order_by('-timestamp')
               

        return render(request, "network/index.html", {
            "NewPostform": NewPostform,
            "posts": posts
        })
    


def profile_view(request, username):

    user = request.user
    profile = User.objects.get(username=username)

    # Get all users that follow this profile
    users_following = profile.followers.all()

    followed = False

    # Check if  current user is following profile
    for user_following in users_following:
        if user_following == user:
            followed = True

    print(followed)



    if request.method == "POST":
        # Handles adding/removing listing from Watchlist
        if request.POST["formtype"] == "follow": 
            profile.followers.add(user)
            
            return redirect("network:profile", username)
        
        elif request.POST["formtype"] == "unfollow":
            profile.followers.remove(user)
            
            return redirect("network:profile", username)
        
        print(followed)
    
    else:
        

        return render(request, "network/profile.html", {
            "profile": profile,
            "followed": followed
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")
    

