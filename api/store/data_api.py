import pandas as pd
from django.db import connection
from store.models import Store, BusinessHour, StoreActivity
from django.db import IntegrityError
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
        self.paths = [self.status_csv_path,
                      self.timezone_csv_path, self.business_csv_path]
        self.batch_size = 10000

        # for path in self.paths:
        # self.add_stores()

        self.transform_csv(self.business_csv_path)
        self.transform_csv(self.status_csv_path)
        print(f"tranform {self.business_csv_path}")

    @staticmethod
    def read_csv(file_path: str) -> csv_data:
        print("running")
        df = pd.read_csv(file_path)
        data: csv_data = df.to_dict(orient='records')
        print("Number of items:", len(data))
        return data

    def transform_csv(self, file_path: str):
        store_df = pd.read_csv(self.timezone_csv_path)
        df = pd.read_csv(file_path)
        # valid_store_ids = Store.objects.values_list('store_id', flat=True)
        df = df[df['store_id'].isin(store_df['store_id'])]
        df.to_csv(file_path, index=False)

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

    def add_business_hours(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                COPY store_businesshour ("store_id", "week_day", "start_time", "end_time")
                FROM %s
                WITH (FORMAT CSV, DELIMITER ',', NUll '', HEADER)
            """, ['/storeAPI/data/hours.csv'])

    def add_stores(self):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                            COPY store_store ("store_id", "timezone")
                            FROM %s
                            WITH (FORMAT CSV, DELIMITER ',', NUll '', HEADER)
                        """, ['/storeAPI/data/timezones.csv'])
        except IntegrityError as e:
            print(f"Stores Are Already Added: {e!s}")

    def add_store_status(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                    COPY store_storeactivity ("store_id", "status", "timestamp")
                    FROM %s
                    WITH (FORMAT CSV, DELIMITER ',', NUll '', HEADER)
                    ON CONFLICT ("store_id") DO UPDATE
                    SET status = EXCLUDED.status, timestamp = EXCLUDED.timestamp
                """, ['/storeAPI/data/status.csv'])
