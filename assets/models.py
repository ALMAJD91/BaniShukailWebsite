from django.db import models

class Asset(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        IN_REPAIR = "IN_REPAIR", "In repair"
        RETIRED = "RETIRED", "Retired"

    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"
