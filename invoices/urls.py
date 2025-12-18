from django.urls import path
from . import views

app_name = "invoices"

urlpatterns = [
    path("invoices/", views.list_invoices, name="list"),
    path("invoices/create/", views.create_invoice, name="create"),
    path("invoices/<int:invoice_id>/print/", views.print_invoice, name="print"),
]
