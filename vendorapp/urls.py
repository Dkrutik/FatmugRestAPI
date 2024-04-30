from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('api/vendors/', VendorCreateAPIView.as_view(), name='vendor-create'),
    path('api/vendorsget/',VendorGetAPIView.as_view(),name='vendor-get'),
    path('api/vendors/<int:vendor_id>/', VendorRetrieveAPIView.as_view(), name='vendor-retrieve'),
    path('api/vendorsput/<int:vendor_id>/', VendorUpdateAPIView.as_view(), name='vendor-update'),
    path('api/vendorsdellet/<int:vendor_id>/', VendorDeleteAPIView.as_view(), name='vendor-delete'),

    path('api/purchase_orders/', PurchaseCreateAPIView.as_view(), name='vendor-create'),
    path('api/purchase_ordersget/',PurchaseGetAPIView.as_view(),name='vendor-get'),
    path('api/purchase_orders/<int:po_id>/', PurchaseRetrieveAPIView.as_view(), name='vendor-retrieve'),
    path('api/purchase_ordersput/<int:po_id>/', PurchaseUpdateAPIView.as_view(), name='vendor-update'),
    path('api/purchase_ordersdellet/<int:po_id>/', PurchaseDeleteAPIView.as_view(), name='vendor-delete'),


    path('api/vendors/<int:vendor_id>/performance/', VendorPerformanceAPIView.as_view(), name='vendor_performance'),
    path('api/purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderAPIView.as_view(), name='acknowledge_purchase_order'),


]
