from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from django.conf import settings
from sales.utils import generate_invoice_pdf
from django.db.models.signals import post_save
from django.dispatch import receiver
User = get_user_model()

class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    stripe_payment_id = models.CharField(max_length=255, blank=True, null=True)  # Store Stripe Payment ID
    created_at = models.DateTimeField(auto_now_add=True)  # Store Order Creation Date

    def __str__(self):
        return f"Order {self.id} - {self.product.name} - {self.status}"

class Invoice(models.Model):
    sales_order = models.OneToOneField(SalesOrder, on_delete=models.CASCADE)
    pdf = models.FileField(upload_to='invoices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for Order {self.sales_order.id}"

@receiver(post_save, sender=Invoice)
def create_invoice_pdf(sender, instance, **kwargs):
    if not instance.pdf:  # Only generate if PDF is not already uploaded
        pdf_path = generate_invoice_pdf(instance)
        instance.pdf = pdf_path
        instance.save()

class Discount(models.Model):
    name = models.CharField(max_length=100)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    product = models.ManyToManyField(Product)
    active = models.BooleanField(default=True)
    valid_until = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.discount_percentage}%"
