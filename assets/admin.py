from django.contrib import admin
from .models import Asset

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("code","name","location","status")
    search_fields = ("code","name","location")
    list_filter = ("status",)
