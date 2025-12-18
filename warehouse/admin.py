from django.contrib import admin
from .models import WarehouseItem

@admin.register(WarehouseItem)
class WarehouseItemAdmin(admin.ModelAdmin):
    list_display = ("code","name","unit_label","price","stock_qty","item_type")
    search_fields = ("code","name")
    list_filter = ("item_type",)
