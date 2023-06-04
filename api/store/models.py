from django.db import models
import datetime


class Store(models.Model):
    store_id = models.BigIntegerField(primary_key=True)
    timezone = models.CharField(max_length=150, default='America/Chicago')

    def __str__(self) -> str:
        return f"Store: {self.store_id}"


class StoreActivity(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    status = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f"StoreActivity: {self.status}"


class BusinessHour(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, null=True, blank=True)
    week_day = models.IntegerField()
    start_time = models.TimeField(default=datetime.time(0, 0, 0))
    end_time = models.TimeField(default=datetime.time(23, 59, 59))

    def __str__(self) -> str:
        return f"BusinessHour: {self.start_time}"
