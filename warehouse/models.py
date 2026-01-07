from django.db import models

class Warehouse(models.Model):
    warehouse_no = models.AutoField(primary_key=True)
    warehouse_name = models.CharField(max_length=200)
    warehouse_location = models.CharField(max_length=200)

    def __str__(self):
        return self.warehouse_name

class WarehouseItem(models.Model):
    location = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True, blank=True)
    class ItemType(models.TextChoices):
        FIXED = "fixed", "Fixed"
        PER_METER = "per_meter", "Per meter"

    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    unit_label = models.CharField(max_length=50, default="piece")  # e.g. متر / رقم
    price = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    stock_qty = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    item_type = models.CharField(max_length=20, choices=ItemType.choices, default=ItemType.FIXED)

    def __str__(self):
        return f"{self.code} - {self.name}"
