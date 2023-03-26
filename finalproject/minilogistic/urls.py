from django.urls import path
from . import views




app_name = "minilogistic"

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('calendar/', views.calendar, name='calendar'),
    path('', views.agenda_view, name='agenda')
]

