from django.contrib import admin
from .models import Customer, Invoice, InvoiceItem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("code","name","wilaya","contact_person")
    search_fields = ("code","name","wilaya")

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("invoice_no","date","customer","operation_order_no")
    search_fields = ("invoice_no","operation_order_no","customer__code","customer__name")
    inlines = [InvoiceItemInline]
