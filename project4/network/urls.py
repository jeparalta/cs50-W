
from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following",views.following, name="following"),
    path("<str:username>", views.profile_view, name="profile"),
    path('edit/<int:post_id>', views.edit_post, name='edit_post'),
    path('like/<int:post_id>', views.like_post, name='like_post')
    
]
