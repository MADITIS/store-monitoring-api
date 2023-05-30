from django.db import models


class Store(models.Model):
    store_id = models.IntegerField(blank=False, null=False)
    status = models.CharField(max_length=30)
    status_timestamp = models.DateTimeField()
    week_day = models.IntegerField()
    start_time_local = models.TimeField()
    end_time_local = models.TimeField()
    store_timezone = models.CharField(max_length=150)


# class StoreStatus(models.Model):
#     store_id = models.IntegerField()
#     timestamp_utc = models.DateTimeField()
#     status = models.CharField(max_length=30)
#     store = models.OneToOneField(Store, on_delete=models.CASCADE)


# class BusinessHours(models.Model):
#     store_id = models.IntegerField()
#     dayOfWeek = models.IntegerField()
#     start_time_local = models.TimeField()
#     end_time_local = models.TimeField()
#     store = models.OneToOneField(Store, on_delete=models.CASCADE)


# class StoreTimezone(models.Model):
#     store_id = models.IntegerField()
#     timezone_str = models.CharField(max_length=150)
#     store = models.OneToOneField(Store, on_delete=models.CASCADE)
