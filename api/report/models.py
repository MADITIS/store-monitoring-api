from django.db import models


class Report(models.Model):
    store_id = models.IntegerField(blank=False, null=False)
    uptime_last_hour = models.IntegerField(blank=False, null=False)
    uptime_last_day = models.IntegerField(blank=False, null=False)
    uptime_last_week = models.IntegerField(blank=False, null=False)
    downtime_last_hour = models.IntegerField(blank=False, null=False)
    downtime_last_day = models.IntegerField(blank=False, null=False)
    downtime_last_week = models.IntegerField(blank=False, null=False)
