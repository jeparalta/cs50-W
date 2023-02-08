from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting",views.newlisting, name="newlisting"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("<str:title>", views.listing_view, name="listing")
    
    
]
