from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    return render(request, "dashboard.html", {
        "title": "Dashboard",
        "subtitle": "Overview of system modules",
        "active": "dashboard",
    })

from warehouse.models import WarehouseItem

@login_required
def reports(request):
    items = WarehouseItem.objects.all().order_by('name')
    return render(request, "reports.html", {
        "title": "Reports",
        "subtitle": "Warehouse Stock Report",
        "active": "reports",
        "items": items,
    })

@login_required
def settings_view(request):
    return render(request, "settings.html", {
        "title": "System Settings",
        "subtitle": "Configure system settings",
        "active": "settings",
    })
