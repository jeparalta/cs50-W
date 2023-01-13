from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.entry, name="entry"),
    path("newpage/", views.newpage, name="newpage"),
    path("edit/", views.edit, name="edit"),
    path("update/", views.update, name="update"),
    path("random/", views.randomchoice, name="random")
]
