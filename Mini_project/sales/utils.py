from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from django.conf import settings

def generate_invoice_pdf(invoice):

    pdf_filename = f"invoice_{invoice.sales_order.id}.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, "invoices", pdf_filename)

    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 14)

    c.drawString(200, 750, "INVOICE")

    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Invoice ID: {invoice.id}")
    c.drawString(100, 680, f"Order ID: {invoice.sales_order.id}")
    c.drawString(100, 660, f"Customer: {invoice.sales_order.customer.username}")
    c.drawString(100, 640, f"Product: {invoice.sales_order.product.name}")
    c.drawString(100, 620, f"Quantity: {invoice.sales_order.quantity}")
    c.drawString(100, 600, f"Total Price: ${invoice.sales_order.price}")

    c.drawString(100, 500, "Thank you for your purchase!")

    c.save()

    invoice.pdf = f"invoices/{pdf_filename}"
    invoice.save()

    return invoice.pdf
