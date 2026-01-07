from django.db import models

class Asset(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        IN_REPAIR = "IN_REPAIR", "In repair"
        RETIRED = "RETIRED", "Retired"

    code = models.CharField(max_length=30, unique=True, blank=True)
    name = models.CharField(max_length=200)
    location = models.ForeignKey("warehouse.Warehouse", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    notes = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.code:
            last = Asset.objects.order_by("id").last()
            new_id = (last.id + 1) if last else 1
            self.code = f"AST-{new_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} - {self.name}"
