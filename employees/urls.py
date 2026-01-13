from django.urls import path
from . import views

app_name = "employees"

urlpatterns = [
    path("employees/", views.list_employees, name="list"),
    path("employees/save/", views.save_employee, name="save"),
    path("employees/delete/<int:emp_id>/", views.delete_employee, name="delete"),
]
