from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone

from .models import LPO, LPOItem
from warehouse.models import WarehouseItem
from invoices.models import Customer


@login_required
def list_lpo(request):
    return render(
        request,
        "lpo.html",
        {
            "title": "LPO / Quotation",
            "subtitle": "Manage LPO & quotations",
            "active": "lpo",
            "lpos": LPO.objects.order_by("-date", "-id"),
        },
    )


@login_required
def create_lpo(request):
    if request.method == "POST":
        lpo_no = request.POST.get("lpo_no", "").strip()
        date_str = request.POST.get("date", "").strip()
        
        # Customer handling
        customer_code = request.POST.get("customer_code", "").strip()
        customer_name = request.POST.get("customer_select", "").strip()
        
        # Other fields
        wilaya_code = request.POST.get("wilaya_code", "").strip()
        location_site = request.POST.get("location_site", "").strip()
        reference_no = request.POST.get("reference_no", "").strip()

        if not lpo_no or not date_str:
            messages.error(request, "LPO No and Date are required.")
        else:
            try:
                date = timezone.datetime.fromisoformat(date_str).date()
            except Exception:
                date = timezone.now().date()

            # Find or Create Customer
            customer = None
            if customer_code:
                customer = Customer.objects.filter(code=customer_code).first()
            
            if not customer and customer_name:
                customer = Customer.objects.filter(name=customer_name).first()
            
            if not customer:
                # Create new customer if meaningful data exists
                if customer_code or customer_name:
                    code_to_use = customer_code or f"CUST-{lpo_no}" # Fallback code
                    name_to_use = customer_name or f"Customer {code_to_use}"
                    customer = Customer.objects.create(
                        code=code_to_use, 
                        name=name_to_use,
                        wilaya=wilaya_code
                    )

            if not customer:
                 messages.error(request, "Please select or enter a valid customer.")
                 return redirect("lpo:create")

            lpo = LPO.objects.create(
                lpo_no=lpo_no,
                date=date,
                customer=customer,
                wilaya_code=wilaya_code,
                location_site=location_site,
                reference_no=reference_no,
                created_by=request.user,
            )

            # items (dynamic rows)
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

            max_len = max(
                len(item_codes),
                len(descriptions),
                len(quantities),
                len(unit_prices),
                len(units),
                len(warehouse_codes),
                0,
            )

            for idx in range(max_len):
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
                        item_code = item_code or str(wh.code)
                        desc = desc or (wh.description or wh.name)
                        unit = unit or wh.unit_label
                        if price == 0:
                            price = wh.price

                LPOItem.objects.create(
                    lpo=lpo,
                    warehouse_item=wh,
                    item_code=item_code,
                    description=desc,
                    quantity=qty,
                    unit=unit,
                    unit_price=price,
                )

            messages.success(request, "LPO saved.")
            return redirect("lpo:list")

    return render(
        request,
        "lpo_create.html",
        {
            "title": "Create LPO",
            "subtitle": "Prepare a new LPO / quotation using items stored in the warehouse.",
            "active": "lpo",
            "warehouse_items": WarehouseItem.objects.all().order_by("code"),
        },
    )


@login_required
def print_lpo(request, lpo_id: int):
    lpo = get_object_or_404(
        LPO.objects.select_related("created_by").prefetch_related("items"),
        id=lpo_id,
    )
    return render(request, "lpo_print.html", {"lpo": lpo})
