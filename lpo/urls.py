from django.urls import path
from . import views

app_name = "lpo"

urlpatterns = [
    path("lpo/", views.list_lpo, name="list"),
    path("lpo/create/", views.create_lpo, name="create"),
    path("lpo/<int:lpo_id>/print/", views.print_lpo, name="print"),
]
