from django.db import models

class Employee(models.Model):
    emp_no = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    base_salary = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    def __str__(self):
        return f"{self.emp_no} - {self.name}"
