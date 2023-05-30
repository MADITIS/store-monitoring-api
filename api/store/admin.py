from django.contrib import admin
from django.contrib.admin import ModelAdmin
from store.models import (
    Store,
    # StoreStatus,
    # BusinessHours,
    # StoreTimezone
)


@admin.register(Store)
class StoreAdmin(ModelAdmin):
    ...


# @admin.register(StoreStatus)
# class StoreStatusAdmin(ModelAdmin):
#     ...


# @admin.register(BusinessHours)
# class BusinessHoursAdmin(ModelAdmin):
#     ...


# @admin.register(StoreTimezone)
# class StoreTimezoneAdmin(ModelAdmin):
#     ...
