from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from datetime import date, timedelta, datetime
import json
import time
from django.template import loader
from django.template.loader import render_to_string

from .models import User, Account, Location, Cleaner, Booking, Contractor, Clean, Selector

# Create your views here.

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("minilogistic:agenda"))
        else:
            return render(request, "minilogistic/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "minilogistic/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("minilogistic:login"))


def register(request):
    if request.method == "POST":
        # Get credentials entered by user
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "minilogistic/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user or return error if username already exists
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "minilogistic/register.html", {
                "message": "Username already taken."
            })
        
        # Create first account for user
        first_account = Account.objects.create(name=f"{user.username}'s Account")
        first_account.save()
        user.accounts_owned.set([first_account])

        login(request, user)
        return HttpResponseRedirect(reverse("minilogistic:agenda"))
    else:
        return render(request, "minilogistic/register.html")

@login_required
def agenda_view(request):

    user = request.user
    bookings = Booking.objects.all().order_by("arrival_date", "arrival_time")
    cleans = Clean.objects.all().order_by("date", "start_time")
    

    #today = date.today() + timedelta(days=12)

    # Last day selected by user
    selected_days = Selector.objects.filter(user = user)
    if selected_days:
        for day in selected_days:
            day = day
    else:
        # Create a new Selector object for user
        new_day = Selector(user=user, agenda_date=date.today())  
        new_day.save()  
        day = new_day

    # Last Agenda format selected by user (Horizontal or Vertical)
    selector = Selector.objects.filter(user=user).first()  
    if selector:  
        agenda_horizontal = selector.agenda_horizontal  
        #print(agenda_horizontal)  
    else:
        print("Selector object not found for user")
    
    # List of the range of days to be displayed
    dates = [day.agenda_date + timedelta(days=i) for i in range(0, 7)]
    
    #print(day)

    return render(request, "minilogistic/agenda.html", {
    
        "bookings": bookings,
        "cleans": cleans,
        #"today": today,
        "dates": dates,
        "day": day,
        "agenda_horizontal": agenda_horizontal
        
    } )


def days(request):
   
    user = request.user

    # Get date selected by user
    selected_date_str = request.GET.get("selected")
    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        dates = [selected_date + timedelta(days=i) for i in range(0, 7)]
    else:
        selected_date = date.today()
        dates = [selected_date + timedelta(days=i) for i in range(0, 7)]

    # Get horizontal toggle value
    horizontal_str = request.GET.get("horizontal", "False")
    horizontal = horizontal_str.lower() == "true"

    # Update Selector model with new date
    selector, created = Selector.objects.get_or_create(user=user)

    # If selector exists, update the date
    if not created:
        selector.agenda_date = selected_date
        selector.save()

    # Get cleans and bookings for the date range
    cleans = Clean.objects.filter(date__range=(dates[0], dates[-1])).order_by("date", "start_time")
    bookings = Booking.objects.filter(arrival_date__range=(dates[0], dates[-1])).order_by("arrival_date", "arrival_time")
    

    # Render the day-section template
    rendered_day_section = render_to_string("minilogistic/day_section.html", {
        "dates": dates,
        "cleans": cleans,
        "bookings": bookings,
        "agenda_horizontal": horizontal,  # Pass the horizontal value to the template context
    })

    # Return the rendered html for the day section
    return JsonResponse({"rendered_day_section": rendered_day_section})


def update_toggle(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    toggle = data.get('toggle')
    print('toggle value:', toggle)  
    
    selector = Selector.objects.get(user=request.user)  
    selector.agenda_horizontal = toggle
    selector.save()
    return JsonResponse({'status': 'success'})
  else:
    return JsonResponse({'status': 'error'})
  

def booking_form(request):
    template = loader.get_template('minilogistic/bookingform.html')
    locations = Location.objects.all()

    return HttpResponse(template.render({
        "locations":locations,
    }, request))


def newclean_form(request):
    template = loader.get_template('minilogistic/newcleanform.html')
    locations = Location.objects.all()
    bookings = Booking.objects.all()
    cleaners = Cleaner.objects.all()

    return HttpResponse(template.render({
        "locations":locations,
        "bookings":bookings,
        "cleaners":cleaners
    }, request))


def new_booking(request):

    if request.method == "POST":
        print("Received location id:", request.POST.get("location"))
        print(request.POST)

        user = request.user


        location = Location.objects.get(id=request.POST.get("location"))
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        arrival_date = request.POST.get("arrival_date")
        departure_date = request.POST.get("departure_date")
        arrival_time_str = request.POST.get("arrival_time")
        arrival_time = datetime.strptime(arrival_time_str, "%H:%M").time()
        
        
        new_booking = Booking(location=location, firstname=firstname, lastname=lastname, arrival_date=arrival_date, arrival_time=arrival_time, departure_date=departure_date)
        new_booking.save()

        return JsonResponse({"status": "success", "message": "Booking added successfully"})
    

def new_clean(request):

    if request.method == "POST":
        
        print(request.POST)

        location = Location.objects.get(id=request.POST.get("location"))
        cleandate = request.POST.get("clean_date")
        start_time = request.POST.get("start_time")
        same_day = request.POST.get("same_day")
        if same_day == "on":
            same_day = "True"
        else:
            same_day = "False"
        arrival_time = request.POST.get("arrival_time")
        if arrival_time == "":
            arrival_time = None
        
        print(same_day)
        #booking = Booking.objects.get(id=request.POST.get("booking_name"))
        #print(booking)

        cleaners_assigned_ids = request.POST.getlist("cleaners_assigned")
        cleaners_assigned = [Cleaner.objects.get(id=cleaner_id) for cleaner_id in cleaners_assigned_ids]
        
        
        new_clean = Clean(location=location, date=cleandate, start_time=start_time, arrival_time=arrival_time, same_day=same_day)
        new_clean.save()

        # Assign cleaners to the new_clean object using set()
        new_clean.cleaners.set(cleaners_assigned)

        return JsonResponse({"status": "success", "message": "Clean added successfully"})
    



    """
    I first need to define how user will navigate between accounts
    HOW TO SHARE AN ACCOUNT 
    EXAMPLE:
    account = Account.objects.get(id=1)
    user = User.objects.get(id=2)
    account.share_with(user, permission_level=PermissionLevel.ADMIN)

    
    """