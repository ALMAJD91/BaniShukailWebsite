from django import forms
from .models import WarehouseItem

class WarehouseItemForm(forms.ModelForm):
    class Meta:
        model = WarehouseItem
        fields = ["location", "code", "name", "description", "unit_label", "price", "stock_qty", "item_type"]
        widgets = {
            "description": forms.TextInput(attrs={"placeholder": "Optional"}),
        }
