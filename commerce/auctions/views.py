from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from decimal import Decimal

from .models import User, Listing, Bid, Comment #Watchlist

class NewListingForm(forms.Form):

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
    price = forms.DecimalField(max_digits=6, decimal_places=2, label="Starting Bid €")
    image = forms.ImageField()

class BidForm(forms.Form):
    bid = forms.DecimalField(max_digits=6, decimal_places=2, label="Bid €")

@login_required
def index(request):

    
    user = request.user
    #print(user)
    #user_listings = Listing.objects.filter(owner=user)

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
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
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

def newlisting(request):
    if request.method == "POST":
        #newtitle = request.post("title")
        #description = request.post("description")
        #price = request.post("price")
        #image = request.post("image")
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid:
            
            listing = Listing(owner = request.user,
                            title=request.POST["title"], 
                            description = request.POST["description"],
                            price = request.POST["price"],
                            image = request.FILES['image']
            )
                            
            listing.save()





            return HttpResponseRedirect(reverse("auctions:index"))



    return render(request, "auctions/newlisting.html", {
        "form": NewListingForm
    })

def listing_view(request, title):
    
    
    user = request.user
    listing = Listing.objects.get(title=title)

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
            return redirect("auctions:listing", title)

    else:
        user = request.user
        # Get all listing data for this title
        listing = Listing.objects.get(title=title)

        # Get all current users watching this listing
        #user_watchlist = Watchlist.objects.filter(user=user)
        users_watching = listing.users_watching.all()

        on_watchlist = False

        # Check if this listing is on user_watchlist 
        for user_watching in users_watching:
            if user_watching == user:
                on_watchlist = True
            
        
            
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "user": user,
            "on_watchlist": on_watchlist,
            "bid_form": BidForm
        })

#def bid(request, title):
    #return
