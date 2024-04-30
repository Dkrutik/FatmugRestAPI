from django.db import models
from django.utils import timezone
# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()


    def update_performance_metrics(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')
        total_completed_orders = completed_orders.count()

        if total_completed_orders > 0:
            # Calculate on-time delivery rate
            on_time_delivery_orders = completed_orders.filter(delivery_date__lte=timezone.now())
            on_time_delivery_rate = on_time_delivery_orders.count() / total_completed_orders

            # Calculate quality rating average
            quality_ratings = completed_orders.exclude(quality_rating__isnull=True).values_list('quality_rating', flat=True)
            quality_rating_avg = sum(quality_ratings) / len(quality_ratings) if quality_ratings else 0

            # Calculate average response time
            response_times = completed_orders.exclude(acknowledgment_date__isnull=True).annotate(response_time=models.F('acknowledgment_date') - models.F('issue_date')).values_list('response_time', flat=True)
            average_response_time = sum(response_times, timezone.timedelta()).total_seconds() / len(response_times) if response_times else 0

            # Calculate fulfillment rate
            fulfilled_orders = completed_orders.filter(delivery_date__lte=timezone.now())
            fulfillment_rate = fulfilled_orders.count() / total_completed_orders

            self.on_time_delivery_rate = on_time_delivery_rate
            self.quality_rating_avg = quality_rating_avg
            self.average_response_time = average_response_time
            self.fulfillment_rate = fulfillment_rate
        else:
            self.on_time_delivery_rate = 0
            self.quality_rating_avg = 0
            self.average_response_time = 0
            self.fulfillment_rate = 0

        self.save()

    def __str__(self):
        return self.name
    
class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField()

    def __str__(self):
        return self.po_number
    
    
class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"
