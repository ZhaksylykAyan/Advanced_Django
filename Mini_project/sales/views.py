from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework.response import Response
from rest_framework.views import APIView
from users.permissions import IsAdmin
from .models import SalesOrder, Invoice, Discount
from django.db import transaction as db_transaction
from .serializers import SalesOrderSerializer, InvoiceSerializer, DiscountSerializer
from rest_framework import serializers
import pdfkit
from django.core.files.base import ContentFile
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import FileResponse
from .utils import generate_invoice_pdf
import os
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

class SalesOrderCreateView(generics.CreateAPIView):
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        if product.quantity_available < quantity:
            raise serializers.ValidationError("Not enough stock available")

        discount = Discount.objects.filter(product=product, active=True).first()
        discount_amount = 0
        if discount:
            discount_amount = (product.price * discount.discount_percentage) / 100

        total_price = (product.price - discount_amount) * quantity

        serializer.save(customer=self.request.user, price=total_price)

        product.quantity_available = F('quantity_available') - quantity
        product.save()

class SalesOrderListView(generics.ListAPIView):
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SalesOrder.objects.filter(customer=self.request.user)

class SalesOrderApprovalView(generics.UpdateAPIView):
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, *args, **kwargs):
        order = get_object_or_404(SalesOrder, id=kwargs["pk"], status="pending")

        with db_transaction.atomic():
            order.status = "approved"
            order.save()

            pdf_content = f"""
            <h1>Invoice for Order #{order.id}</h1>
            <p>Product: {order.product.name}</p>
            <p>Quantity: {order.quantity}</p>
            <p>Total Price: ${order.price}</p>
            <p>Customer: {order.customer.username}</p>
            """

            pdf_file = pdfkit.from_string(pdf_content, False)
            invoice = Invoice.objects.create(sales_order=order)
            invoice.pdf.save(f"invoice_{order.id}.pdf", ContentFile(pdf_file))

        return Response({"message": "Order approved and invoice generated", "invoice_id": invoice.id}, status=status.HTTP_200_OK)

class InvoiceGenerateView(generics.CreateAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(SalesOrder, id=kwargs["pk"], status="approved")

        pdf_content = f"""
        <h1>Invoice for Order #{order.id}</h1>
        <p>Product: {order.product.name}</p>
        <p>Quantity: {order.quantity}</p>
        <p>Total Price: ${order.price}</p>
        <p>Customer: {order.customer.username}</p>
        """

        pdf_file = pdfkit.from_string(pdf_content, False)
        invoice = Invoice.objects.create(sales_order=order)
        invoice.pdf.save(f"invoice_{order.id}.pdf", ContentFile(pdf_file))

        return Response({"message": "Invoice generated", "invoice_id": invoice.id}, status=status.HTTP_201_CREATED)

class DiscountListView(generics.ListAPIView):
    serializer_class = DiscountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Discount.objects.filter(active=True)

class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")

        order = get_object_or_404(SalesOrder, id=order_id, customer=request.user)

        try:
            # Create a PaymentIntent in Stripe
            intent = stripe.PaymentIntent.create(
                amount=int(order.price * 100),
                currency="usd",
                payment_method_types=["card"],
                metadata={"order_id": order.id}
            )

            return Response({"client_secret": intent.client_secret}, status=status.HTTP_201_CREATED)

        except stripe.error.StripeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = json.loads(payload)
    except json.JSONDecodeError as e:
        return JsonResponse({"error": str(e)}, status=400)

    if event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        order_id = payment_intent["metadata"]["order_id"]

        try:
            order = SalesOrder.objects.get(id=order_id)
            order.status = "paid"
            order.save()

            # Generate invoice
            invoice, created = Invoice.objects.get_or_create(sales_order=order)
            generate_invoice_pdf(invoice)

        except SalesOrder.DoesNotExist:
            return JsonResponse({"error": "Order not found"}, status=404)

    return JsonResponse({"status": "success"})


class DownloadInvoiceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            invoice = Invoice.objects.get(sales_order__id=order_id)
            file_path = os.path.join(settings.MEDIA_ROOT, invoice.pdf.name)

            if os.path.exists(file_path):
                return FileResponse(open(file_path, "rb"), content_type="application/pdf")

            return Response({"error": "File not found"}, status=status.HTTP_404_NOT_FOUND)

        except Invoice.DoesNotExist:
            return Response({"error": "Invoice not found"}, status=status.HTTP_404_NOT_FOUND)