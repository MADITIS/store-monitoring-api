from typing import Dict, List, Tuple
from store.models import BusinessHour
from store.models import Store, StoreActivity
import pytz
import datetime
from core.redis import cache_report, add_report_key
from django.db.models import F


class Report:
    def generate_report(self, report_id):
        add_report_key(report_id)
        reports = []
        stores = Store.objects.all()

        for store in stores:
            result = self.uptime_last_hour(store)
            if result:
                uptime_last_hour, downtime_last_hour = result
            else:
                return
            hours = self.calculate_uptime_downtime(store)

            store_report = {
                'store': store.store_id,
                'uptime_last_hour': uptime_last_hour,
                'downtime_last_hour': downtime_last_hour,
                **hours,
            }

            reports.append(store_report)
        if reports:
            cache_report(report=reports, report_id=report_id, )

    def uptime_last_hour(self, store: Store):
        store_id: int = store.store_id

        current_datetime = datetime.datetime.now(pytz.timezone(store.timezone))
        last_hour_end = current_datetime.time()

        previous_datetime = current_datetime - datetime.timedelta(hours=1)
        last_hour_start = previous_datetime.time()

        try:
            business_hour = BusinessHour.objects.get(
                store__store_id=store_id,
                week_day=current_datetime.weekday()
            )

        except BusinessHour.DoesNotExist:
            print("BusinessHour does not exist")
            return

        if business_hour.end_time < last_hour_end and business_hour.end_time <= last_hour_start:
            return
        if business_hour.start_time >= last_hour_end and business_hour.start_time >= last_hour_start:
            return

        # list of stores at that same weekday
        current_date = current_datetime.date()
        stores = StoreActivity.objects.filter(
            store__store_id=store_id, timestamp__date=current_date).annotate(time=F('timestamp__time'), status=F('status')).values()

        if not stores.exists():
            latest_date = StoreActivity.objects.filter(store__store_id=store_id).order_by(
                "-timestamp__date").values_list("timestamp__date", flat=True).first()
            stores = StoreActivity.objects.filter(
                store__store_id=store_id, timestamp__date=latest_date).annotate(time=F('timestamp__time'), status=F('status')).values()

        return self.__interpolate(business_hour, stores,
                                  last_hour_start, last_hour_end)

    def __interpolate(self, business_hour: BusinessHour, stores, last_hour_start, last_hour_end):
        downtime_last_hour = 0
        uptime_last_hour = 0
        start_hour = business_hour.start_time
        end_hour = business_hour.end_time

        intervals: List[Dict[str, datetime.time]] = [
            {"start": start_hour},
            {"end": end_hour},
        ]
        for i in stores:
            uptime: datetime.time = i['time']
            status: str = i['status']
            if business_hour.end_time <= uptime or business_hour.start_time >= uptime:
                continue

            match status:
                case 'active':
                    intervals.append({
                        status: uptime,
                    })
                case 'inactive':
                    intervals.append(
                        {
                            status: uptime
                        }
                    )
        intervals.sort(key=lambda x: list(x.values())[0])
        if not intervals:
            downtime_last_hour = datetime.datetime.strptime(str(business_hour.end_time), '%H:%M:%S').time(
            ).hour - datetime.datetime.strptime(str(business_hour.start_time), '%H:%M:%S').time().minute
        if last_hour_end > end_hour:
            last_hour_end = end_hour
        elif last_hour_start < start_hour:
            last_hour_start = start_hour
            uptime_last_hour = datetime.datetime.strptime(str(last_hour_end), '%H:%M:%S').time(
            ).hour - datetime.datetime.strptime(str(last_hour_start), '%H:%M:%S').time().minute

        for i in range(1, len(intervals)):
            interval_start = list(intervals[i-1].values())[0]
            interval_end = list(intervals[i].values())[0]
            interval_status = list(intervals[i].keys())[0]

            if interval_start <= last_hour_start and interval_end >= last_hour_end:
                if interval_status == 'active':
                    uptime_last_hour += (datetime.datetime.combine(datetime.date.today(), last_hour_end) -
                                         datetime.datetime.combine(datetime.date.today(), last_hour_start)).total_seconds() / 60
                else:
                    downtime_last_hour += (datetime.datetime.combine(datetime.date.today(), last_hour_end) -
                                           datetime.datetime.combine(datetime.date.today(), last_hour_start)).total_seconds() / 60
            elif interval_start <= last_hour_start < interval_end:
                if interval_status == 'active':
                    uptime_last_hour += (datetime.datetime.combine(datetime.date.today(), interval_end) -
                                         datetime.datetime.combine(datetime.date.today(), last_hour_start)).total_seconds() / 60
                else:
                    downtime_last_hour += (datetime.datetime.combine(datetime.date.today(), interval_end) -
                                           datetime.datetime.combine(datetime.date.today(), last_hour_start)).total_seconds() / 60
            elif interval_start < last_hour_end <= interval_end:
                if interval_status == 'active':
                    uptime_last_hour += (datetime.datetime.combine(datetime.date.today(), last_hour_end) -
                                         datetime.datetime.combine(datetime.date.today(), interval_start)).total_seconds() / 60
                else:
                    downtime_last_hour += (datetime.datetime.combine(datetime.date.today(), last_hour_end) -
                                           datetime.datetime.combine(datetime.date.today(), interval_start)).total_seconds() / 60

        return uptime_last_hour, downtime_last_hour

    @staticmethod
    def calculate_time_diff(start_time, end_time):
        diff = datetime.datetime.combine(datetime.date.today(
        ), end_time) - datetime.datetime.combine(datetime.date.today(), start_time)
        return diff.total_seconds() / 3600

    def calculate_uptime_downtime(self, store):
        current_datetime = datetime.datetime.now(pytz.timezone(store.timezone))
        uptime_last_day = 0
        downtime_last_day = 0
        uptime_last_week = 0
        downtime_last_week = 0

        last_day_start = current_datetime - datetime.timedelta(days=1)
        last_week_start = current_datetime - datetime.timedelta(weeks=1)

        try:
            business_hour = BusinessHour.objects.get(
                store__store_id=store.store_id,
                week_day=current_datetime.weekday()
            )

        except BusinessHour.DoesNotExist:
            print("BusinessHour does not exist")
            return

        prev_time = business_hour.start_time
        prev_status = None

        activities = StoreActivity.objects.filter(
            store=store).order_by('timestamp')

        for activity in activities:
            store_time = activity.timestamp.time()
            store_status = activity.status

            if store.business_hour.start_time <= store_time <= store.business_hour.end_time:
                if prev_status is not None:
                    time_diff = Report.calculate_time_diff(
                        prev_time, store_time)

                    if last_day_start <= activity.timestamp <= current_datetime:
                        if prev_status == 'active':
                            uptime_last_day += time_diff
                        else:
                            downtime_last_day += time_diff

                    if last_week_start <= activity.timestamp <= current_datetime:
                        if prev_status == 'active':
                            uptime_last_week += time_diff
                        else:
                            downtime_last_week += time_diff

                prev_time = store_time
                prev_status = store_status

        if prev_status is not None:
            time_diff = Report.calculate_time_diff(
                prev_time, store.business_hour.end_time)

            if last_day_start <= current_datetime:
                if prev_status == 'active':
                    uptime_last_day += time_diff
                else:
                    downtime_last_day += time_diff

            if last_week_start <= current_datetime:
                if prev_status == 'active':
                    uptime_last_week += time_diff
                else:
                    downtime_last_week += time_diff

        return {"uptime_last_day": uptime_last_day, "downtime_last_day": downtime_last_day,
                "uptime_last_week": uptime_last_week, "downtime_last_week": downtime_last_week}
