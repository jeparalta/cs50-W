from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment

class NewListingForm(forms.Form):

    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    description = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))
    price = forms.DecimalField(max_digits=6, decimal_places=2, label="Starting Bid $")
    image = forms.ImageField()


@login_required
def index(request):

    
    user = request.user

    #print(user)
    #user_listings = Listing.objects.filter(owner=user)
    listings = Listing.objects.all()
    
    return render(request, "auctions/index.html", {
        "listings": listings   #Listing.objects.all()
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def newlisting(request):
    if request.method == "POST":
        #newtitle = request.post("title")
        #description = request.post("description")
        #price = request.post("price")
        #image = request.post("image")
        form = NewListingForm(data=request.POST, files=request.FILES)
        if form.is_valid:
            listing = Listing(owner = request.user,
                            title=request.POST["title"], 
                            description = request.POST["description"],
                            price = request.POST["price"],
                            image = f"static/auctions/{request.POST['image']}")
                            
            listing.save()





            return HttpResponseRedirect(reverse("auctions:index"))



    return render(request, "auctions/newlisting.html", {
        "form": NewListingForm
    })
