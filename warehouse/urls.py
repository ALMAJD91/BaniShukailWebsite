from django.urls import path
from . import views

app_name = "warehouse"

urlpatterns = [
    path("warehouse/", views.list_items, name="list"),
    path("warehouse/add/", views.create_item, name="add"),
    path("warehouse/<int:item_id>/edit/", views.edit_item, name="edit"),
    path("warehouse/<int:item_id>/delete/", views.delete_item, name="delete"),
]
