from django.db import models
from django.contrib.auth.models import User


class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="inventory_items")

    def __str__(self):
        return f"{self.name} ({self.quantity})"

