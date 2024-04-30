from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor
from .serializers import *
from datetime import datetime
from django.utils import timezone
# Create your views here.

class VendorCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VendorGetAPIView(APIView):
    def get(self,request):
        result = Vendor.objects.all()  
        serializers = VendorSerializer(result, many=True)  
        contex = {
            'data': serializers.data,
            'messasge': "Get all vendor data successfully",
            'status': True
            }
        return Response(contex, status=200)  
    
class VendorRetrieveAPIView(APIView):
    def get_object(self, vendor_id):
        try:
            return Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, vendor_id, format=None):
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    


class VendorUpdateAPIView(APIView):
    def get_object(self, vendor_id):
        try:
            return Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return None

    def put(self, request, vendor_id, format=None):
        vendor = self.get_object(vendor_id)
        if vendor is None:
            return Response({"message": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VendorDeleteAPIView(APIView):
    def delete(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return Response({'message': 'Vendor does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        vendor.delete()
        return Response({'message': 'Vendor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    

 
#####################   PurchaseOrder realted API #############################
class PurchaseCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PurchaseGetAPIView(APIView):
    def get(self,request):
        result = PurchaseOrder.objects.all()  
        serializers = PurchaseOrderSerializer(result, many=True)  
        contex = {
            'data': serializers.data,
            'messasge': "Get all PurchaseOrder data successfully",
            'status': True
            }
        return Response(contex, status=200)  



class PurchaseRetrieveAPIView(APIView):
    def get_object(self, po_id):
        try:
            return PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            raise Http404

    def get(self, request, po_id, format=None):
        vendor = self.get_object(po_id)
        serializer = PurchaseOrderSerializer(vendor)
        return Response(serializer.data)
    

class PurchaseUpdateAPIView(APIView):
    def get_object(self, po_id):
        try:
            return PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            return None

    def put(self, request, po_id, format=None):
        vendor = self.get_object(po_id)
        if vendor is None:
            return Response({"message": "PurchaseOrder not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PurchaseOrderSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PurchaseDeleteAPIView(APIView):
    def delete(self, request, po_id):
        try:
            vendor = PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return Response({'message': 'PurchaseOrder does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
        vendor.delete()
        return Response({'message': 'PurchaseOrder deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
#########################3
# class VendorPerformanceAPIView(APIView):
#     def get(self, request, vendor_id):
#         try:
#             vendor = Vendor.objects.get(id=vendor_id)
#             performance_metrics = {
#                 'on_time_delivery_rate': vendor.on_time_delivery_rate,
#                 'quality_rating_avg': vendor.quality_rating_avg,
#                 'average_response_time': vendor.average_response_time,
#                 'fulfillment_rate': vendor.fulfillment_rate,
#             }
#             return Response(performance_metrics)
#         except Vendor.DoesNotExist:
#             return Response(status=404)

class VendorPerformanceAPIView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            performance_metrics = {
                'on_time_delivery_rate': vendor.on_time_delivery_rate,
                'quality_rating_avg': vendor.quality_rating_avg,
                'average_response_time': vendor.average_response_time,
                'fulfillment_rate': vendor.fulfillment_rate,
            }
            return Response(performance_metrics)
        except Vendor.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        



# class AcknowledgePurchaseOrderAPIView(APIView):
#     def acknowledge(self, purchase_order):
      
#         purchase_order.acknowledgment_date = datetime.now()
#         purchase_order.save()

#         purchase_order.Vendor.update_performance_metrics()
#     def post(self, request, po_id):
#         try:
#             purchase_order = PurchaseOrder.objects.get(id=po_id)
#             self.acknowledge(purchase_order)
#             return Response(status=status.HTTP_200_OK)
#         except PurchaseOrder.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

class AcknowledgePurchaseOrderAPIView(APIView):
    def post(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()
            vendor = purchase_order.vendor
            vendor.update_performance_metrics()

            return Response({"message": "Purchase order acknowledged successfully"}, status=status.HTTP_200_OK)
        except PurchaseOrder.DoesNotExist:
            return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)