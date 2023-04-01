from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from datetime import date, timedelta, datetime
import json
import time
from django.template import loader
from django.template.loader import render_to_string

from .models import User, Location, Cleaner, Booking, Contractor, Clean, Selector

# Create your views here.

def agenda_view(request):

    user = request.user
    bookings = Booking.objects.all()
    cleans = Clean.objects.all()
    

    #today = date.today() + timedelta(days=12)

    # Last day selected by user
    selected_days = Selector.objects.filter(user = user)
    for day in selected_days:
        day = day 

    # List of the range of days to be displayed
    dates = [day.agenda_date + timedelta(days=i) for i in range(0, 14)]
    
    #print(day)

    return render(request, "minilogistic/agenda.html", {
    
        "bookings": bookings,
        "cleans": cleans,
        #"today": today,
        "dates": dates,
        "day": day
        
    } )


def days(request):
    # Get user
    user = request.user
    # Get date selected by user
    selected_date_str = request.GET.get("selected")
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    dates = [selected_date + timedelta(days=i) for i in range(0, 14)]

    #print(dates)
    # Update Selector model with new date
    selector, created = Selector.objects.get_or_create(user=user)

    # If selector exists, update the date
    if not created:
        selector.agenda_date = selected_date
        selector.save()

    # Get cleans and bookings for the date range
    cleans = Clean.objects.filter(date__range=(dates[0], dates[-1]))
    bookings = Booking.objects.filter(arrival_date__range=(dates[0], dates[-1]))

    # Render the day-section template
    rendered_day_section = render_to_string("minilogistic/day_section.html", {
        "dates": dates,
        "cleans": cleans,
        "bookings": bookings,
    })

    # Artificially delay speed of response
    #time.sleep(0.5)

    # Return the rendered html for the day section
    return JsonResponse({"rendered_day_section": rendered_day_section})


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
        arrival_time = request.POST.get("arrival_time")
        #booking = Booking.objects.get(id=request.POST.get("booking_name"))
        #print(booking)

        cleaners_assigned_ids = request.POST.getlist("cleaners_assigned")
        cleaners_assigned = [Cleaner.objects.get(id=cleaner_id) for cleaner_id in cleaners_assigned_ids]
        
        
        new_clean = Clean(location=location, date=cleandate, start_time=start_time, arrival_time=arrival_time)
        new_clean.save()

        # Assign cleaners to the new_clean object using set()
        new_clean.cleaners.set(cleaners_assigned)

        return JsonResponse({"status": "success", "message": "Clean added successfully"})