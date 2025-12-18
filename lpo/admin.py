from django.contrib import admin
from .models import LPO, LPOItem

class LPOItemInline(admin.TabularInline):
    model = LPOItem
    extra = 0

@admin.register(LPO)
class LPOAdmin(admin.ModelAdmin):
    list_display = ("lpo_no","date","customer")
    search_fields = ("lpo_no","customer__code","customer__name")
    inlines = [LPOItemInline]
