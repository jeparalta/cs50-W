from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
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

from .models import User, Account, AccountUser, PermissionLevel, Location, Cleaner, Booking, Contractor, Clean, Selector, Comment, ColorCode

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
        first_account = Account.objects.create(name=f"{user.username}'s Account", created_by=user)
        first_account.save()
        

        # Give user ADMIN permission to this account
        account_user = AccountUser.objects.create(user=user, account=first_account, permission_level=PermissionLevel.ADMIN)
        account_user.save()

        # Create Selector object for user
        selector = Selector.objects.create(user=user, account=first_account)
        selector.save()

        login(request, user)
        return HttpResponseRedirect(reverse("minilogistic:agenda"))
    else:
        return render(request, "minilogistic/register.html")

@login_required
def agenda_view(request):

    user = request.user

    # Get account that is currently selected
    selector = Selector.objects.filter(user=user).first()
    selected_account= selector.account

    # Get Bookings and Cleans for selected account
    bookings = Booking.objects.filter(account=selected_account).order_by("arrival_date", "arrival_time")
    cleans = Clean.objects.filter(account=selected_account).order_by("date", "start_time")
    

    #today = date.today() + timedelta(days=12)

    # Get selector that belongs to user
    selector = Selector.objects.filter(user = user)

    if selector:
        for day in selector:
            day = day.agenda_date
    else:
        # if user doesnt have a selector assigned yet then Create a new Selector
        new_day = Selector(user=user, agenda_date=date.today())  
        new_day.save()  
        day = new_day.agenda_date

    # Last Agenda format selected by user (Horizontal or Vertical)
    selector = Selector.objects.filter(user=user).first()  
    if selector:  
        agenda_horizontal = selector.agenda_horizontal  
        #print(agenda_horizontal)  
    else:
        print("Selector object not found for user")
    
    # List of the range of days to be displayed
    dates = [day + timedelta(days=i) for i in range(0, 14)]
    
    print("day variable is:", day)

    return render(request, "minilogistic/agenda.html", {
    
        "bookings": bookings,
        "cleans": cleans,
        #"today": today,
        "dates": dates,
        "day": day,
        "agenda_horizontal": agenda_horizontal
        
    } )


def settings_view(request):

    user = request.user
    # Get accounts that user has access to
    account_users = AccountUser.objects.filter(user=user)
    accounts = [account_user.account for account_user in account_users]

    # Get account that is currently selected
    selector = Selector.objects.filter(user=user).first()
    selected_account= selector.account


    return render(request, "minilogistic/settings.html", {
        "accounts": accounts,
        "selected_account": selected_account 
    })

def fullday_view(request, day):

    user = request.user
    # Get account that is currently selected
    selector = Selector.objects.filter(user=user).first()
    selected_account= selector.account

    # Convert the day string to a date object
    day_date = datetime.strptime(day, "%Y-%m-%d").date()
    print("day:", day)
    print("day_date:", day_date)

    # Get all bookings and cleans of this account from this day
    bookings = Booking.objects.filter(arrival_date=day_date, account=selected_account).order_by("arrival_date", "arrival_time")
    cleans = Clean.objects.filter(date=day_date, account=selected_account).order_by("date", "start_time")
    

    return render(request, "minilogistic/fullday.html", {
        "day":day_date,
        "bookings":bookings,
        "cleans":cleans
    })

def fullday(request):
    

    user = request.user
    # Get account that is currently selected
    selector = Selector.objects.filter(user=user).first()
    selected_account= selector.account


    # Get date for full day view
    day_date_str = request.GET.get("selected")
    print("DateSTR:",day_date_str)
    if day_date_str:
        day_date = datetime.strptime(day_date_str, "%Y-%m-%d").date()
        print("date:", day_date)
    else:
        day_date = date.today()

    # Update Selector model with new date
    selector, created = Selector.objects.get_or_create(user=user)

    # If selector exists, update the date
    if not created:
        selector.agenda_date = day_date
        selector.save()

    #print(selector.agenda_date)
        

    # Get all bookings and cleans of this account from this day
    bookings = Booking.objects.filter(arrival_date=day_date, account=selected_account).order_by("arrival_date", "arrival_time")
    cleans = Clean.objects.filter(date=day_date, account=selected_account).order_by("date", "start_time")
    
    print(bookings)


    rendered_fullday_section = render_to_string("minilogistic/fullday_section.html", {
        "day":day_date,
        "bookings":bookings,
        "cleans":cleans
    })

    return HttpResponse(rendered_fullday_section)


def days(request):
   
    user = request.user
    # Get account that is currently selected
    selector = Selector.objects.filter(user=user).first()
    selected_account= selector.account

    #print(selected_account)

    # Get date selected by user
    selected_date_str = request.GET.get("selected")
    if selected_date_str:
        selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        dates = [selected_date + timedelta(days=i) for i in range(0, 14)]
    else:
        selected_date = date.today()
        dates = [selected_date + timedelta(days=i) for i in range(0, 14)]

    # Get horizontal toggle value
    horizontal_str = request.GET.get("horizontal", "False")
    horizontal = horizontal_str.lower() == "true"

    # Update Selector model with new date
    selector, created = Selector.objects.get_or_create(user=user)

    # If selector exists, update the date
    if not created:
        selector.agenda_date = selected_date
        selector.save()

    # Get cleans and bookings for the selected account in the date range
    cleans = Clean.objects.filter(date__range=(dates[0], dates[-1]), account=selected_account).order_by("date", "start_time")
    bookings = Booking.objects.filter(arrival_date__range=(dates[0], dates[-1]), account=selected_account).order_by("arrival_date", "arrival_time")
    
    print(selected_date)

    # Render the day-section template
    rendered_day_section = render_to_string("minilogistic/day_section.html", {
        "day": selected_date,
        "dates": dates,
        "cleans": cleans,
        "bookings": bookings,
        "agenda_horizontal": horizontal,  # Pass the horizontal value to the template context
    })

    # Return the rendered html for the day section
    #return JsonResponse({"rendered_day_section": rendered_day_section})
    return HttpResponse(rendered_day_section)


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
    user = request.user
    # Get account that is currently selected
    selector = Selector.objects.filter(user=user).first()
    selected_account= selector.account

    template = loader.get_template('minilogistic/bookingform.html')
    locations = Location.objects.filter(account=selected_account)

    return HttpResponse(template.render({
        "locations":locations,
    }, request))


def newclean_form(request):
    user = request.user
    # Get account that is currently selected
    selector = Selector.objects.filter(user=user).first()
    selected_account= selector.account

    template = loader.get_template('minilogistic/newcleanform.html')
    locations = Location.objects.filter(account=selected_account)
    cleaners = Cleaner.objects.filter(account=selected_account)

    return HttpResponse(template.render({
        "locations":locations,
        "cleaners":cleaners
    }, request))

def editclean_form(request, cleanid):
    user = request.user
    # Get account that is currently selected
    selector = Selector.objects.filter(user=user).first()
    selected_account= selector.account

    # Get clean to be edited
    clean = Clean.objects.filter(id=cleanid).first()

    template = loader.get_template('minilogistic/editcleanform.html')

    # Get locations and options for this user account
    locations = Location.objects.filter(account=selected_account)
    cleaners = Cleaner.objects.filter(account=selected_account)

    # Get existing data for this clean

    return HttpResponse(template.render({
        "locations":locations,
        "cleaners":cleaners,
        "clean":clean
    }, request))


def new_booking(request):

    if request.method == "POST":
        print("Received location id:", request.POST.get("location"))
        print(request.POST)

        user = request.user

        # Get account that is currently selected by user
        selector = Selector.objects.filter(user=user).first()
        account= selector.account

       
        location = Location.objects.get(id=request.POST.get("location"))
        firstname = request.POST.get("first_name")
        lastname = request.POST.get("last_name")
        arrival_date = request.POST.get("arrival_date")
        departure_date = request.POST.get("departure_date")
        arrival_time_str = request.POST.get("arrival_time")
        arrival_time = datetime.strptime(arrival_time_str, "%H:%M").time()
        
        
        new_booking = Booking(account=account, location=location, firstname=firstname, lastname=lastname, arrival_date=arrival_date, arrival_time=arrival_time, departure_date=departure_date, added_by=user)
        new_booking.save()

        return JsonResponse({"status": "success", "message": "Booking added successfully"})
    

def new_clean(request):

    if request.method == "POST":
        
        #print("request Post:", request.POST)

        user = request.user

        # Get account that is currently selected by user
        selector = Selector.objects.filter(user=user).first()
        account= selector.account

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
        
        #print(same_day)
        #booking = Booking.objects.get(id=request.POST.get("booking_name"))
        #print(booking)

        cleaners_assigned_ids = request.POST.getlist("cleaners_assigned[]")
        cleaners_assigned = [Cleaner.objects.get(id=cleaner_id) for cleaner_id in cleaners_assigned_ids]
        
        
        new_clean = Clean(account=account, location=location, date=cleandate, start_time=start_time, arrival_time=arrival_time, same_day=same_day, added_by=user)
        new_clean.save()

        print(cleaners_assigned)
        # Assign cleaners to the new_clean object using set()
        new_clean.cleaners.set(cleaners_assigned)

        return JsonResponse({"status": "success", "message": "Clean added successfully"})
    
def add_comment(request):
    if request.method == "POST":

        user = request.user

        # Get account that is currently selected by user
        selector = Selector.objects.filter(user=user).first()
        account = selector.account
        booking_id = request.POST.get("bookingId")
        print("Booking ID:", booking_id)


        clean = Clean.objects.filter(id=request.POST.get("cleanId")).first() # need to retreive cleanId from addcomment form
        booking = Booking.objects.filter(id=request.POST.get("bookingId")).first() # need to retrieve bookingId from addcomment form
        

        body = request.POST.get("comment_body")
        color = request.POST.get("comment_color")
        color_code = ColorCode[color.upper()].value

        if clean:
            new_comment = Comment(account=account, commenter=user, clean_belong=clean, body=body, color=color_code)
        elif booking:
            new_comment = Comment(account=account, commenter=user, booking_belong=booking, body=body, color=color_code)

        new_comment.save()

        comment_serialized = serialize('json', [new_comment])


        return JsonResponse({"status": "success", "message": "Comment added successfully", "comment": comment_serialized})







"""
    
    HOW TO SHARE AN ACCOUNT 
    EXAMPLE:
    account = Account.objects.get(id=1)
    user = User.objects.get(id=2)
    account.share_with(user, permission_level=PermissionLevel.ADMIN)

    
"""