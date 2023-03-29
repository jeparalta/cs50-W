from django.urls import path
from . import views




app_name = "minilogistic"

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('calendar/', views.calendar, name='calendar'),
    path('', views.agenda_view, name='agenda'),
    path('days', views.days, name='days'),
    path('bookingform.html', views.booking_form, name='bookingform'),
    path('newcleanform.html', views.newclean_form, name='newcleanform')
]

