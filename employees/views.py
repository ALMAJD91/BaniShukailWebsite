from datetime import date, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Employee
from .forms import EmployeeForm

@login_required
def list_employees(request):
    employees = Employee.objects.all().order_by("emp_no")
    
    # Filter by search term
    q = request.GET.get("q", "")
    if q:
        employees = employees.filter(
            Q(name__icontains=q) |
            Q(nationality__icontains=q) | 
            Q(emp_no__icontains=q)
        )

    # Filter by nationality
    nationality = request.GET.get("nationality", "")
    if nationality and nationality != "All":
        employees = employees.filter(nationality__iexact=nationality)

    warning_date = date.today() + timedelta(days=30)

    return render(request, "employees.html", {
        "title": "Employees",
        "subtitle": "Employee list and payroll basics",
        "active": "employees",
        "employees": employees,
        "search_q": q,
        "selected_nationality": nationality,
        "warning_date": warning_date,
    })

@login_required
def save_employee(request):
    if request.method == "POST":
        emp_id = request.POST.get("emp_id")
        if emp_id:
            employee = get_object_or_404(Employee, id=emp_id)
            form = EmployeeForm(request.POST, instance=employee)
        else:
            form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Employee saved successfully.")
        else:
            messages.error(request, "Error saving employee. Please check the form.")
    
    return redirect("employees:list")

@login_required
def delete_employee(request, emp_id):
    employee = get_object_or_404(Employee, id=emp_id)
    employee.delete()
    messages.success(request, "Employee deleted successfully.")
    return redirect("employees:list")
