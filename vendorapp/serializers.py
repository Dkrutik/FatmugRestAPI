from rest_framework import serializers
from .models import *

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_details', 'address', 'vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']



class PurchaseOrderSerializer(serializers.ModelSerializer):
    order_date = serializers.DateTimeField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
    delivery_date=serializers.DateTimeField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
    acknowledgment_date= serializers.DateTimeField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
    issue_date = serializers.DateTimeField(format='%Y-%m-%d', input_formats=['%Y-%m-%d'])
    class Meta:
        model=PurchaseOrder
        fields="__all__"