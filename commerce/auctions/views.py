from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from decimal import Decimal


from .models import User, Listing, Bid, Comment, Category 


"""FORMS"""
class NewListingForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":"5", 'class': 'form-control'}))
    price = forms.DecimalField(max_digits=6, decimal_places=2, label="Starting Bid €", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), to_field_name='name', required=True, widget=forms.Select(attrs={'class': 'form-control'}))

class BidForm(forms.Form):
    bid = forms.DecimalField(max_digits=6, decimal_places=2, label="Bid €")

class CommentForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    body = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))


@login_required
def index(request):

    # Get current user and all existing active listings from db
    user = request.user
    active_listings = Listing.objects.filter(active=True)
    
    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
        "user": user 
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:login"))


def register(request):
    if request.method == "POST":
        # Get credentials entered by user
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user or return error if username already exists
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def newlisting(request):

    if request.method == "POST":
        # request info from form
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid:
            
            listing = Listing(owner = request.user,
                            title=request.POST["title"], 
                            description = request.POST["description"],
                            price = request.POST["price"],
                            category = Category.objects.get(name=request.POST['category']),
                            image = request.FILES['image']
            )               
            listing.save()

        return HttpResponseRedirect(reverse("auctions:index"))

    else:
        # Get all categories to display on New Listing Form options
        categories = Category.objects.all()

        return render(request, "auctions/newlisting.html", {
            "form": NewListingForm,
            "categories":categories
        })

@login_required
def listing_view(request, title):
    
    user = request.user
    listing = Listing.objects.get(title=title)
    comments = listing.listing_comments.all()

    # Get all current users watching this listing
    users_watching = listing.users_watching.all()

    on_watchlist = False

    # Check if this listing is on user_watchlist 
    for user_watching in users_watching:
        if user_watching == user:
            on_watchlist = True

    if request.method == "POST":
        
        # Handles adding/removing listing from Watchlist
        if request.POST["formtype"] == "add": 
            user.watchlist.add(listing)
            return redirect("auctions:listing", title)
        elif request.POST["formtype"] == "remove":
            user.watchlist.remove(listing)
            return redirect("auctions:listing", title)

        # Handles bids    
        elif request.POST["formtype"] == "bid":
            bid = Decimal(request.POST["bid"])
            if listing.price >= bid:
                return render(request, "auctions/listing.html", {
                "listing": listing,
                "user": user,
                "on_watchlist": on_watchlist,
                "bid_form": BidForm,
                "message" : f"Your bid must be higher than €{listing.price}"
                })
            else:
                listing.price = request.POST["bid"]
                listing.bid_count+=1
                listing.current_winner = user
                listing.save()
                # Record bid 
                new_bid = Bid(bidder=user, listing=listing, amount=bid)
                new_bid.save()
                return redirect("auctions:listing", title)
        # Handles closing the listing if the user is the owner
        elif request.POST["formtype"] == "close":
                listing.active = False
                listing.save()
                return redirect("auctions:listing", title)

        # Handles Comments
        elif request.POST["formtype"] == "comment":
            comment_title = request.POST["title"]
            comment_body = request.POST["body"]

            new_comment = Comment(commenter=user, listing=listing, title=comment_title, body=comment_body)
            new_comment.save()
            return redirect("auctions:listing", title)


    else:
        
        # Get all current users watching this listing
        users_watching = listing.users_watching.all()

        on_watchlist = False

        # Check if this listing is on user_watchlist 
        for user_watching in users_watching:
            if user_watching == user:
                on_watchlist = True
            
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "user": user,
            "comments": comments,
            "on_watchlist": on_watchlist,
            "bid_form": BidForm,
            "comment_form": CommentForm
        })

@login_required
def watchlist(request):
    # Define user and identify which listings are on users watchlist
    user = request.user
    user_watchlist = user.watchlist.all()
    
    return render(request, "auctions/watchlist.html", {
        "user": user,
        "user_watchlist": user_watchlist
    })

@login_required
def categories(request):

    categories = Category.objects.all()

    return render(request, "auctions/categories.html", {
        "categories": categories
    })

@login_required
def category_view(request, name):
    
    # Get selected category
    category = Category.objects.get(name=name)
    # Get all active listings with selected category
    active_listings = Listing.objects.filter(category=category, active=True)

    return render(request, "auctions/category.html", {
        "category": category,
        "active_listings": active_listings
    })

