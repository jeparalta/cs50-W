from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django import forms
import json



from .models import User, Post, Comment


"""FORMS"""
class NewPostform(forms.Form):
    body = forms.CharField(label="", widget=forms.Textarea(attrs={"rows":"5", "class": "form-control"}))
    

"""VIEWS"""
def index(request):

    if request.method == "POST":
        form = NewPostform(request.POST)
        if form.is_valid:
            newpost = Post(poster = request.user, body = request.POST["body"])
            newpost.save()
        return HttpResponseRedirect(reverse("network:index"))

    else:
        posts = Post.objects.all().order_by('-timestamp')

        # Paginator
        page_number = request.GET.get('page', 1)
        paginator = Paginator(posts, 10)
        page = paginator.get_page(page_number)    

        return render(request, "network/index.html", {
            "NewPostform": NewPostform,
            "page": page,
            "heading": "All Posts"
        })


@login_required
def following(request):

    if request.method == "POST":
        form = NewPostform(request.POST)
        if form.is_valid:
            newpost = Post(poster = request.user, body = request.POST["body"])
            newpost.save()
        return HttpResponseRedirect(reverse("network:index"))

    else:
        user = request.user
        followedprofiles = user.following.all()
        posts = []
        
        # Populate list of posts user follows
        for followedprofile in followedprofiles:
            posts_from_profile = Post.objects.filter(poster = followedprofile)
                
            for post in posts_from_profile:
                posts.append(post)

        # Sort the posts in descending order
        posts = sorted(posts, key=lambda x: x.timestamp, reverse=True)                      

        # Paginator
        page_number = request.GET.get('page', 1)
        paginator = Paginator(posts, 10)
        page = paginator.get_page(page_number)
               

        return render(request, "network/index.html", {
            "NewPostform": NewPostform,
            "page": page,
            "heading": "Following"
        })
    


def profile_view(request, username):

    user = request.user
    profile = User.objects.get(username=username)

    # Get all users that follow this profile
    users_following = profile.followers.all()

    # Initiate followed variable to false
    followed = False

    # Check if  current user is following profile and update followed if true
    for user_following in users_following:
        if user_following == user:
            followed = True

    if request.method == "POST":

        # Handles following/unfollowing
        if request.POST["formtype"] == "follow": 
            profile.followers.add(user)
            return redirect("network:profile", username)
        
        elif request.POST["formtype"] == "unfollow":
            profile.followers.remove(user)
            return redirect("network:profile", username)
    
    else:

        posts = Post.objects.filter(poster=profile).order_by('-timestamp')

        #Paginator
        page_number = request.GET.get('page', 1)
        paginator = Paginator(posts, 10)
        page = paginator.get_page(page_number)
        
        return render(request, "network/profile.html", {
            "profile": profile,
            "followed": followed,
            "page": page
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



def edit_post(request, post_id):

    if request.method == 'PUT':
        # update the post
        post = Post.objects.get(id=post_id)
        user = request.user

        if post.poster == user:

            body = request.body.decode('utf-8')
            post_data = json.loads(body)
            post.body = post_data['body']
            post.save()

            # return a JSON response
            response_data = {'success': True}
            return JsonResponse(response_data)



def like_post(request, post_id):
    if request.method == "PUT":
    
            # Get post
            post = Post.objects.get(id=post_id)
            user = request.user

            # Check if the user already liked the post
            if user in post.liked_by.all():
                post.liked_by.remove(user)
            else:
                post.liked_by.add(user)

            post.save()

            # Return a JSON response
            response_data = {'success': True}
            return JsonResponse(response_data)
    
    
def booking_form(request):
    template = loader.get_template('minilogistic/booking_form.html')
    return HttpResponse(template.render({}, request))

        
    
    




        

    

