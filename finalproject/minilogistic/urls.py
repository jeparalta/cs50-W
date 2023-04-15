from django.urls import path
from . import views


app_name = "minilogistic"

urlpatterns = [
    
    path('', views.agenda_view, name='agenda'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('days/', views.days, name='days'),
    path('bookingform.html/', views.booking_form, name='bookingform'),
    path('newcleanform.html/', views.newclean_form, name='newcleanform'),
    path('minilogistic/newbooking/', views.new_booking, name='newbooking'),
    path('minilogistic/newclean/', views.new_clean, name='newclean'),
    path('update-toggle/', views.update_toggle, name='update_toggle'),
    path('settings/', views.settings_view, name="settings"),
    path('fullday/<str:day>/', views.fullday_view, name='fullday'),
    path('fulldaybody/', views.fullday, name='fulldaybody'),
    path('add-comment/', views.add_comment, name='addcomment')
]

