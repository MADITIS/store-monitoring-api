from django.db import models
import datetime
# from postgres_copy import CopyManager


# class Store(models.Model):
#     store_id = models.BigIntegerField(blank=False, null=False, unique=True)
#     status = models.CharField(max_length=30, null=True)
#     status_timestamp = models.DateTimeField(null=True)
#     week_day = models.IntegerField(null=True)
#     start_time_local = models.TimeField(null=True)
#     end_time_local = models.TimeField(null=True)
#     store_timezone = models.CharField(max_length=150, null=True)


class Store(models.Model):
    store_id = models.BigIntegerField(primary_key=True)
    timezone = models.CharField(max_length=150, default='America/Chicago')


class StoreActivity(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=30)


class BusinessHour(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, null=True, blank=True)
    week_day = models.IntegerField()
    start_time = models.TimeField(default=datetime.time(0, 0, 0))
    end_time = models.TimeField(default=datetime.time(23, 59, 59))
