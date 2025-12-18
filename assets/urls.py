from django.urls import path
from . import views

app_name = "assets"

urlpatterns = [
    path("assets/", views.list_assets, name="list"),
]
