from django.db import models

# Create your models here.
class CustomerOrder(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("SHIPPED", "Shipped"),
        ("CANCELED", "Canceled"),
        ("COMPLETED", "Completed"),
    )

    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField(null=True, blank=True)
    customer_phone = models.CharField(max_length=30, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    notes = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order-{self.id} ({self.customer_name})"
    
class CustomerOrderItem(models.Model):
    customer_order = models.ForeignKey(
        "CustomerOrder",
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey("inventory.Product", on_delete=models.PROTECT)

    quantity = models.PositiveIntegerField()
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)    

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"