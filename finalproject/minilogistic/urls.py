from django.urls import path
from . import views


app_name = "minilogistic"

urlpatterns = [
    
    path('', views.agenda_view, name='agenda'),
    path('days', views.days, name='days'),
    path('bookingform.html', views.booking_form, name='bookingform'),
    path('newcleanform.html', views.newclean_form, name='newcleanform'),
    path('minilogistic/newbooking', views.new_booking, name='newbooking'),
    path('minilogistic/newclean', views.new_clean, name='newclean'),
]

