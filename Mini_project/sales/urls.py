from django.urls import path
from .views import (
    SalesOrderCreateView, SalesOrderListView, SalesOrderApprovalView,
    InvoiceGenerateView, DiscountListView, CreatePaymentIntentView, stripe_webhook, DownloadInvoiceView
)

urlpatterns = [
    path('sales_order/create/', SalesOrderCreateView.as_view(), name='sales-order-create'),
    path('sales_order/list/', SalesOrderListView.as_view(), name='sales-order-list'),
    path('sales_order/approve/<int:pk>/', SalesOrderApprovalView.as_view(), name='sales-order-approve'),
    path('invoice/generate/<int:pk>/', InvoiceGenerateView.as_view(), name='invoice-generate'),
    path('discounts/', DiscountListView.as_view(), name='discount-list'),
    path('payment/create/', CreatePaymentIntentView.as_view(), name="create-payment-intent"),
    path("stripe/webhook/", stripe_webhook, name="stripe-webhook"),
    path("invoice/download/<int:order_id>/", DownloadInvoiceView.as_view(), name="download-invoice"),
]
