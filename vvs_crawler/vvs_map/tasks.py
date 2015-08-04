__author__ = 'fritz'
import requests
from .models import MapEntry
import datetime
from vvs_crawler.celery import app


@app.task(bind=True)
def get_json(args):
    binary = requests.get('http://m.vvs.de/VELOC')
    json = binary.json()


    for entry in json:
        timestamp_before = unix_timestamp_to_datetime(entry.get("TimestampBefore")[6:16])

        day_of_operation = unix_timestamp_to_datetime(entry.get("DayOfOperation")[6:16])
        timestamp = unix_timestamp_to_datetime(entry.get("Timestamp")[6:16])

        vvs_id = entry.get("ID")
        direction_text = entry.get("DirectionText")
        line_text = entry.get("LineText")
        longitude = entry.get("Longitude")
        latitude_before = entry.get("LatitudeBefore", "")
        is_at_stop = entry.get("IsAtStop")
        journey_id = entry.get("JourneyIdentifier")
        delay = entry.get("Delay")
        current_stop = entry.get("CurrentStop")
        product_id = entry.get("ProductIdentifier")
        mod_code = entry.get("ModCode")
        real_time_available = entry.get("RealtimeAvailable")
        longitude_before = entry.get("LongitudeBefore")

        operator = entry.get("Operator")
        latitude = entry.get("Latitude")
        next_stop = entry.get("NextStop")
        if not is_at_stop:
            is_at_stop = False
        else:
            is_at_stop = True
        MapEntry.objects.create(timestamp=timestamp,
                                day_of_operation=day_of_operation,
                                timestamp_before=timestamp_before,
                                vvs_id=vvs_id,
                                direction_text=direction_text,
                                line_text=line_text,
                                longitude=longitude,
                                latitude_before=latitude_before,
                                is_at_stop=is_at_stop,
                                journey_id=journey_id,
                                delay=delay,
                                current_stop=current_stop,
                                product_id=product_id,
                                mod_code=mod_code,
                                real_time_available=real_time_available,
                                longitude_before=longitude_before,
                                operator=operator,
                                latitude=latitude,
                                next_stop=next_stop
        )


def unix_timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp))