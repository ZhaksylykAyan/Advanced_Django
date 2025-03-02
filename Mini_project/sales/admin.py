from django.contrib import admin
from .models import SalesOrder, Invoice, Discount

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "customer", "product", "quantity", "price", "status", "created_at", "stripe_payment_id")
    list_filter = ("status", "created_at")
    search_fields = ("customer__username", "product__name")
    actions = ["approve_orders", "process_orders"]

    def mark_as_paid(self, request, queryset):
        """ Mark selected orders as Paid """
        queryset.update(status="paid")
        self.message_user(request, "Selected orders marked as Paid.")

    mark_as_paid.short_description = "Mark selected orders as Paid"

    def generate_invoice(self, request, queryset):
        """ Generate invoices for selected orders """
        for order in queryset:
            Invoice.objects.create(sales_order=order, pdf="invoices/sample.pdf")  # Update path dynamically
        self.message_user(request, "Invoices generated for selected orders.")

    generate_invoice.short_description = "Generate invoices for selected orders"

    def approve_orders(self, request, queryset):
        queryset.update(status="approved")
    approve_orders.short_description = "Approve selected orders"

    def process_orders(self, request, queryset):
        queryset.update(status="processed")
    process_orders.short_description = "Process selected orders"

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "sales_order", "pdf", "created_at")
    search_fields = ("sales_order__customer__username", "sales_order__product__name")

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("name", "discount_percentage", "active", "valid_until")
    list_filter = ("active", "valid_until")
    search_fields = ("name", "product__name")
