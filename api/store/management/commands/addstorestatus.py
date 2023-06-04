from store.models import StoreActivity
from django.core.management.base import BaseCommand

from store.data_api import DataAPI

data_api = DataAPI()


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print(f"Adding Stores Activities")
        data_api.add_store_status()
