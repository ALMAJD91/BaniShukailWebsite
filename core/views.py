from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def dashboard(request):
    return render(request, "dashboard.html", {
        "title": "Dashboard",
        "subtitle": "Overview of system modules",
        "active": "dashboard",
    })

@login_required
def reports(request):
    return render(request, "reports.html", {
        "title": "Reports",
        "subtitle": "Generate reports",
        "active": "reports",
    })

@login_required
def settings_view(request):
    return render(request, "settings.html", {
        "title": "System Settings",
        "subtitle": "Configure system settings",
        "active": "settings",
    })
