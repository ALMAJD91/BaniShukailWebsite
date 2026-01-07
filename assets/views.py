from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Asset
from warehouse.models import Warehouse

@login_required
def list_assets(request):
    if request.method == "POST":
        name = request.POST.get("name")
        code = request.POST.get("code")
        location_id = request.POST.get("location")
        status = request.POST.get("status")
        notes = request.POST.get("notes") # Using notes for extra info since fields were removed
        
        if name:
            location = None
            if location_id:
                location = Warehouse.objects.filter(pk=location_id).first()
                
            Asset.objects.create(
                code=code or "", # Model handles auto-generation if empty
                name=name,
                location=location,
                status=status or Asset.Status.ACTIVE,
                notes=notes or ""
            )
            messages.success(request, "Asset added successfully.")
            return redirect("assets:list")
            
    return render(request, "assets.html", {
        "title": "Assets",
        "subtitle": "Track company assets and their status",
        "active": "assets",
        "assets": Asset.objects.select_related("location").order_by("code"),
        "warehouses": Warehouse.objects.all(),
    })
