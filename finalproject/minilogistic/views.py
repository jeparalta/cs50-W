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

def hello():

    return HttpResponse("Hello, World!")



def calendar(request):
    
    return render(request, "minilogistic/calendar.html")



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

    # Return the rendered HTML
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
    return HttpResponse(template.render({
        "locations":locations,
        "bookings": bookings
    }, request))