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
        self.status_csv_path: str = os.path.join(self.data_dir, 'status.csv')
        self.timezone_csv_path: str = os.path.join(self.data_dir, 'timezones.csv')
        self.business_csv_path: str = os.path.join(self.data_dir, 'hours.csv')

    def transform_csv(self, file_path: str):
        '''
        Removes the redundant rows
        '''
        store_df = pd.read_csv(self.timezone_csv_path)
        df = pd.read_csv(file_path)
        df = df[df['store_id'].isin(store_df['store_id'])]
        df.to_csv(file_path, index=False)
        print("transformed")

    def add_business_hours(self):
        self.transform_csv(self.business_csv_path)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    COPY store_businesshour ("store_id", "week_day", "start_time", "end_time")
                    FROM %s
                    WITH (FORMAT CSV, DELIMITER ',', NUll '', HEADER)
                """, ['/storeAPI/data/hours.csv'])
        except IntegrityError as e:
            print("Business Hour already added")

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
        self.transform_csv(self.status_csv_path)
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                        COPY store_storeactivity ("store_id", "status", "timestamp")
                        FROM %s
                        WITH (FORMAT CSV, DELIMITER ',', NUll '', HEADER)
                    """, ['/storeAPI/data/status.csv'])
        except IntegrityError as e:
            print("Status Already Added, Now updating status")
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TEMPORARY TABLE temp_store_activity
                    (
                        store_id bigint,
                        status varchar(255),
                        timestamp timestamp
                    )
                """)

                cursor.execute("""
                    COPY temp_store_activity ("store_id", "status", "timestamp")
                    FROM %s
                    WITH (FORMAT CSV, DELIMITER ',', NULL '', HEADER)
                """, ['/storeAPI/data/status.csv'])

                cursor.execute("""
                    UPDATE store_storeactivity AS s
                    SET status = t.status, timestamp = t.timestamp
                    FROM temp_store_activity AS t
                    WHERE s.store_id = t.store_id
                """)
