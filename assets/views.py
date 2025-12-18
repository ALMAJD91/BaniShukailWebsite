from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Asset

@login_required
def list_assets(request):
    return render(request, "assets.html", {
        "title": "Assets",
        "subtitle": "Track company assets and their status",
        "active": "assets",
        "assets": Asset.objects.order_by("code"),
    })
