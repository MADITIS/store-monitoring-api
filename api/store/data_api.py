import csv
import os
from typing import Dict, Iterator, List
from store.models import Store


class DataAPI:
    path: str = os.path.abspath(__file__)
    parent_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(path)))
    data_dir: str = os.path.join(parent_dir, 'data')

    def __init__(self):
        self.status_data = os.path.join(self.data_dir, 'status.csv')
        self.timezone_data = os.path.join(self.data_dir, 'timezones.csv')
        self.business_hours_data = os.path.join(self.data_dir, 'hours.csv')

    def store_status_data(self):
        with open(self.status_data, "r") as status_file:
            csv_reader: Iterator[Dict[str, str]] = csv.DictReader(status_file)
            for line in csv_reader:
                Store.objects.create(
                    store_id=line['store_id'],
                    status=line['status'],
                    status_timestamp=line['timestamp_utc'],
                )
