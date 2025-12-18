from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("emp_no","name","job_title","phone","base_salary")
    search_fields = ("emp_no","name")
