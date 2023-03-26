from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from datetime import date, timedelta

from .models import User, Location, Cleaner, Booking, Contractor, Clean

# Create your views here.

def hello():

    return HttpResponse("Hello, World!")



def calendar(request):
    
    return render(request, "minilogistic/calendar.html")



def agenda_view(request):

    bookings = Booking.objects.all()
    cleans = Clean.objects.all()
    today = date.today() + timedelta(days=12)
    
    dates = [today + timedelta(days=i) for i in range(0, 7)]
    


    return render(request, "minilogistic/agenda.html", {
        "bookings": bookings,
        "cleans": cleans,
        "today": today,
        "dates": dates
    } )

