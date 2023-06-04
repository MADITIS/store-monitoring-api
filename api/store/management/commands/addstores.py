from store.models import StoreActivity
from django.core.management.base import BaseCommand, CommandError

from store.data_api import DataAPI

data_api = DataAPI()
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print(f"Adding Stores")
        data_api.add_stores()
