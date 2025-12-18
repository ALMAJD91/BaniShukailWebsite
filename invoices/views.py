import json
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from .models import Invoice, InvoiceItem, Customer
from warehouse.models import WarehouseItem

def _warehouse_items_json():
    data = {}
    for it in WarehouseItem.objects.all().order_by("code"):
        data[str(it.code)] = {
            "code": str(it.code),
            "name": it.name,
            "description": it.description or it.name,
            "unitLabel": it.unit_label,
            "price": float(it.price),
            "type": it.item_type,
        }
    return json.dumps(data)

@login_required
def list_invoices(request):
    return render(request, "invoices.html", {
        "title": "Invoices",
        "subtitle": "Manage invoices",
        "active": "invoices",
        "invoices": Invoice.objects.select_related("customer").order_by("-date", "-id"),
    })

@login_required
def create_invoice(request):
    if request.method == "POST":
        invoice_no = request.POST.get("invoice_no","").strip()
        date_str = request.POST.get("date","").strip()
        operation_order_no = request.POST.get("operation_order_no","").strip()
        customer_code = request.POST.get("customer_code","").strip()
        customer_name = (request.POST.get("customer_select","") or "").strip()
        wilaya_code = request.POST.get("wilaya_code","").strip()
        location_site = request.POST.get("location_site","").strip()

        if not invoice_no or not customer_code or not date_str:
            messages.error(request, "Invoice No, Date, and Customer Code are required.")
        else:
            # customer
            cust, _ = Customer.objects.get_or_create(code=customer_code, defaults={
                "name": customer_name or f"Customer {customer_code}",
                "wilaya": wilaya_code,
                "address": location_site,
            })
            # parse date
            try:
                date = timezone.datetime.fromisoformat(date_str).date()
            except Exception:
                date = timezone.now().date()

            inv = Invoice.objects.create(
                invoice_no=invoice_no,
                date=date,
                operation_order_no=operation_order_no,
                customer=cust,
                wilaya_code=wilaya_code,
                location_site=location_site,
                created_by=request.user,
            )

            # items (dynamic rows)
# Preferred: repeated field names so we can use getlist()
warehouse_codes = request.POST.getlist("warehouse_code")
item_codes = request.POST.getlist("item_code")
descriptions = request.POST.getlist("description")
quantities = request.POST.getlist("quantity")
units = request.POST.getlist("unit")
unit_prices = request.POST.getlist("unit_price")

# Backward compatibility (older template had only 2 rows with suffixes)
if not any([warehouse_codes, item_codes, descriptions, quantities, units, unit_prices]):
    for i in (1, 2):
        warehouse_codes.append((request.POST.get(f"warehouse_code_{i}") or "").strip())
        item_codes.append((request.POST.get(f"item_code_{i}") or "").strip())
        descriptions.append((request.POST.get(f"description_{i}") or "").strip())
        quantities.append((request.POST.get(f"quantity_{i}") or "0").strip())
        units.append((request.POST.get(f"unit_{i}") or "").strip())
        unit_prices.append((request.POST.get(f"unit_price_{i}") or "0").strip())

for idx in range(max(len(item_codes), len(descriptions), len(quantities), len(unit_prices), len(units), len(warehouse_codes))):
    code = (warehouse_codes[idx] if idx < len(warehouse_codes) else "").strip()
    item_code = (item_codes[idx] if idx < len(item_codes) else "").strip()
    desc = (descriptions[idx] if idx < len(descriptions) else "").strip()
    unit = (units[idx] if idx < len(units) else "").strip()

    try:
        qty = Decimal((quantities[idx] if idx < len(quantities) else "0") or "0")
    except Exception:
        qty = Decimal("0")

    try:
        price = Decimal((unit_prices[idx] if idx < len(unit_prices) else "0") or "0")
    except Exception:
        price = Decimal("0")

    if not (item_code or desc or code) and qty == 0:
        continue

    wh = None
    if code:
        wh = WarehouseItem.objects.filter(code=code).first()
        if wh:
            item_code = item_code or wh.code
            desc = desc or (wh.description or wh.name)
            unit = unit or wh.unit_label
            if price == 0:
                price = wh.price

    InvoiceItem.objects.create(
        invoice=inv,
        warehouse_item=wh,
        item_code=item_code,
        description=desc,
        quantity=qty,
        unit=unit,
        unit_price=price,
    )

messages.success(request, "Invoice saved.")
            return redirect("invoices:list")

    return render(request, "invoice_create.html", {
        "title": "Create Invoice",
        "subtitle": "Prepare a new tax invoice using items stored in the warehouse.",
        "active": "invoices",
        "warehouse_items_json": _warehouse_items_json(),
        "warehouse_items": WarehouseItem.objects.all().order_by("code"),
    })

@login_required
def print_invoice(request, invoice_id: int):
    invoice = get_object_or_404(Invoice.objects.select_related("customer","created_by").prefetch_related("items"), id=invoice_id)
    return render(request, "invoice_print.html", {"invoice": invoice})
