from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import WarehouseItem
from .forms import WarehouseItemForm

def _require_admin(user) -> bool:
    return getattr(user, "is_admin", lambda: False)()

@login_required
def list_items(request):
    return render(request, "warehouse.html", {
        "title": "Warehouse Items",
        "subtitle": "Manage stock items, unit prices, and quantities.",
        "active": "warehouse",
        "items": WarehouseItem.objects.order_by("code"),
    })

@login_required
def create_item(request):
    if not _require_admin(request.user):
        messages.error(request, "Only Admin can add or edit warehouse items.")
        return redirect("warehouse:list")

    if request.method == "POST":
        form = WarehouseItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Warehouse item added.")
            return redirect("warehouse:list")
    else:
        form = WarehouseItemForm()

    return render(request, "warehouse_form.html", {
        "title": "Add Warehouse Item",
        "active": "warehouse",
        "form": form,
        "mode": "create",
    })

@login_required
def edit_item(request, item_id: int):
    if not _require_admin(request.user):
        messages.error(request, "Only Admin can add or edit warehouse items.")
        return redirect("warehouse:list")

    item = get_object_or_404(WarehouseItem, id=item_id)

    if request.method == "POST":
        form = WarehouseItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Warehouse item updated.")
            return redirect("warehouse:list")
    else:
        form = WarehouseItemForm(instance=item)

    return render(request, "warehouse_form.html", {
        "title": "Edit Warehouse Item",
        "active": "warehouse",
        "form": form,
        "mode": "edit",
        "item": item,
    })

@login_required
def delete_item(request, item_id: int):
    if not _require_admin(request.user):
        messages.error(request, "Only Admin can delete warehouse items.")
        return redirect("warehouse:list")

    item = get_object_or_404(WarehouseItem, id=item_id)
    if request.method == "POST":
        item.delete()
        messages.success(request, "Warehouse item deleted.")
        return redirect("warehouse:list")

    return render(request, "warehouse_delete_confirm.html", {
        "title": "Delete Warehouse Item",
        "active": "warehouse",
        "item": item,
    })
