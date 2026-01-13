from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "emp_no", "name", "nationality", "job_title", "phone",
            "date_joined", "passport_expiry", "labour_card_expiry",
            "base_salary", "notes"
        ]
        widgets = {
            "date_joined": forms.DateInput(attrs={"type": "date"}),
            "passport_expiry": forms.DateInput(attrs={"type": "date"}),
            "labour_card_expiry": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
