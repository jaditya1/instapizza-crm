from django.db import models

# Create your models here.
from Orders.models import Order
from django.contrib.postgres.fields import ArrayField,JSONField


class Client_details(models.Model):
    client_id = models.CharField(max_length=200,blank=False,null=False,verbose_name="Client Id")
    client_token = models.CharField(max_length=1000,blank=False,null=False,verbose_name="Client Token")
    created_at = models.DateTimeField(blank=True, null=True,
                                                        verbose_name='Creation Date & Time')
    updated_at = models.DateTimeField(blank=True, null=True,
                                                        verbose_name='Updation Date & Time')

    class Meta:
        verbose_name = "Client Details"
        verbose_name_plural = "Client Details"

    def __str__(self):
        return str(self.client_id)


class Unprocessed_Order_Quote(models.Model):
    order_quote_id = models.ForeignKey(Order,related_name='Unprocessed_Order_Quote_Order_Id',on_delete=models.CASCADE,verbose_name='OrderId')
    raw_api_response = JSONField(blank=True,null=True,verbose_name="Quote Response")
    created_at = models.DateTimeField(blank=True, null=True,
                                                        verbose_name='Creation Date & Time')
    updated_at = models.DateTimeField(blank=True, null=True,
                                                        verbose_name='Updation Date & Time')

    class Meta:
        verbose_name = "Unprocessed Order Quote"
        verbose_name_plural = "Unprocessed Order Qoute"

    def __str__(self):
        return str(self.order_quote_id)

class Processed_Order_Quote(models.Model):
    order_quote_id = models.ForeignKey(Order,related_name='processed_Order_Quote_Order_Id',on_delete=models.CASCADE,verbose_name='OrderId')
    category_id = models.CharField(max_length=100,blank=True,null=True,verbose_name="CategoryId Details")
    distance = models.FloatField(blank=True,null=True,verbose_name="Distance Details")
    estimated_price = models.FloatField(blank=True,null=True,verbose_name="Estimated Price Details")
    eta = JSONField(blank=True,null=True,verbose_name="Pickup Dropoff Details")
    created_at = models.DateTimeField(blank=True, null=True,
                                                        verbose_name='Creation Date & Time')
    updated_at = models.DateTimeField(blank=True, null=True,
                                                        verbose_name='Updation Date & Time')

    class Meta:
        verbose_name = "Processed Order Quote"
        verbose_name_plural = "Processed Order Quote"

    def __str__(self):
        return str(self.order_quote_id)

class Order_Task(models.Model):
    order_id = models.ForeignKey(Order,related_name='Order_Task_Id',on_delete=models.CASCADE,verbose_name='OrderId')
    task_id = models.CharField(max_length=200,blank=False,null=False,verbose_name="TaskId Details")
    request_id = models.CharField(max_length=200,blank=False,null=False,verbose_name="RequestId Details")
    state = models.CharField(max_length=100,blank=False,null=False,verbose_name="State Details")
    reference_id = models.CharField(max_length=100,blank=True,null=True,verbose_name="ReferenceId Details")
    estimated_price = models.FloatField(blank=True,null=True,verbose_name="Estimated Price Details")
    eta = JSONField(blank=True,null=True,verbose_name="Pickup Dropoff Details")
    created_at = models.DateTimeField(blank=True, null=True,
                                                        verbose_name='Creation Date & Time')
    updated_at = models.DateTimeField(blank=True, null=True,
                                                        verbose_name='Updation Date & Time')

    class Meta:
        verbose_name = "Order Task"
        verbose_name_plural = "Order Task"

    def __str__(self):
        return str(self.order_id)


class Task_State_Updates(models.Model):
    event_type = models.CharField(max_length=200,blank=False,null=False,verbose_name="Event Type Details")
    event_id = models.CharField(max_length=200,blank=False,null=False,verbose_name="Event Id Details")
    task_id = models.CharField(max_length=200,blank=False,null=False,verbose_name="Task Id")
    reference_id = models.CharField(max_length=200,blank=True,null=True,verbose_name="Reference Id Details")
    state = models.CharField(max_length=100,blank=False,null=False,verbose_name="State Details")
    # event_timestamp = models.DateTimeField(verbose_name='Event Date & Time')
    eta = JSONField(blank=True,null=True,verbose_name="Pickup Dropoff Details")
    price = models.FloatField(blank=True,null=True,verbose_name="Price Details")
    total_time = models.FloatField(blank=True,null=True,verbose_name="Total Time")
    cancelled_by = models.CharField(max_length=100,blank=True,null=True,verbose_name="Cancelled By")
    cancellation_reason = models.CharField(max_length=500,blank=True,null=True,verbose_name="Cancellation Reason")
    runner = JSONField(blank=True,null=True,verbose_name="Runner Details")
    created_at = models.DateTimeField(blank=True, null=True,
                                                        verbose_name='Creation Date & Time')
    updated_at = models.DateTimeField(blank=True, null=True,
                                                        verbose_name='Updation Date & Time')
    # request_timestamp = models.DateTimeField(verbose_name='Request Date & Time')

    class Meta:
        verbose_name = "Task State Updates "
        verbose_name_plural = "Task State Updates"

    def __str__(self):
        return str(self.task_id)







