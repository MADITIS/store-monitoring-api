import pandas as pd
from store.models import Store
from typing import Any, Dict, Hashable, Iterator, List, Tuple
import os
import pandas as pd
from datetime import datetime, tzinfo
from dateutil import parser


csv_data = List[Dict[Hashable, Any]]


class DataAPI:
    path: str = os.path.abspath(__file__)
    parent_dir: str = os.path.dirname(os.path.dirname(os.path.dirname(path)))
    data_dir: str = os.path.join(parent_dir, 'data')

    def __init__(self):
        self.status_csv_path = os.path.join(self.data_dir, 'status.csv')
        self.timezone_csv_path = os.path.join(self.data_dir, 'timezones.csv')
        self.business_csv_path = os.path.join(self.data_dir, 'hours.csv')
        self.batch_size = 1000

    @staticmethod
    def read_csv(file_path: str) -> csv_data:
        print("running")
        df = pd.read_csv(file_path)
        # df.drop_duplicates(
        #     subset=['store_id', 'timestamp_utc'], inplace=True)
        data: csv_data = df.to_dict(orient='records')
        print(len(data))
        return data

    def store_status_data(self):
        data = DataAPI.read_csv(self.status_csv_path)

        stores = (
            Store(
                store_id=i['store_id'],
                status=i['status'],
                status_timestamp=parser.parse(i['timestamp_utc']),
            )
            for i in data[:self.batch_size]
        )
        Store.objects.bulk_create(
            stores, update_conflicts=['status', 'status_timestamp'],
            unique_fields=['store_id'],
            update_fields=['status', 'status_timestamp'],
            batch_size=self.batch_size,
        )

    def add_stores(self):
        data = DataAPI.read_csv(self.timezone_csv_path)
        stores = (
            Store(
                store_id=store['store_id'],
                timezone=store['timezone_str']
            )
            for store in data
        )

        Store.objects.bulk_create(
            stores
        )
