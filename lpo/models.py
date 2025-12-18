from django.db import models
from django.conf import settings
from warehouse.models import WarehouseItem
from invoices.models import Customer

class LPO(models.Model):
    lpo_no = models.CharField(max_length=50, unique=True)
    date = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="lpos")
    subject = models.CharField(max_length=200, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    vat_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.00)

    def subtotal(self):
        return sum([it.amount for it in self.items.all()])

    def vat_amount(self):
        return (self.subtotal() * (self.vat_rate/100))

    def total(self):
        return self.subtotal() + self.vat_amount()

    def __str__(self):
        return self.lpo_no

class LPOItem(models.Model):
    lpo = models.ForeignKey(LPO, on_delete=models.CASCADE, related_name="items")
    warehouse_item = models.ForeignKey(WarehouseItem, on_delete=models.SET_NULL, null=True, blank=True)
    item_code = models.CharField(max_length=30, blank=True)
    description = models.CharField(max_length=500, blank=True)
    quantity = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    unit = models.CharField(max_length=50, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    @property
    def amount(self):
        return self.quantity * self.unit_price
