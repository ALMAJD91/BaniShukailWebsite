from django.db import models

class Employee(models.Model):
    emp_no = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    nationality = models.CharField(max_length=100, blank=True)
    date_joined = models.DateField(null=True, blank=True)
    passport_expiry = models.DateField(null=True, blank=True)
    labour_card_expiry = models.DateField(null=True, blank=True)
    base_salary = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.emp_no} - {self.name}"
