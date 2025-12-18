from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Employee

@login_required
def list_employees(request):
    return render(request, "employees.html", {
        "title": "Employees",
        "subtitle": "Employee list and payroll basics",
        "active": "employees",
        "employees": Employee.objects.order_by("emp_no"),
    })
