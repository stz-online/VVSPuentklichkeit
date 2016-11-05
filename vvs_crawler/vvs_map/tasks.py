__author__ = 'fritz'
import requests
from .models import VVSData, VVSJourney, VVSTransport, Stop, Line, Direction
import datetime
from vvs_crawler.celery import app
from pytz import UTC
from django.contrib.gis.geos import Point
from django.core.cache import cache
import sendgrid
import os
from YamJam import yamjam
import tweepy
from django.db import IntegrityError
from django.db.models import Max
import redis
from operator import itemgetter

MOD_RBAHN=0
MOD_SBAHN=1
MOD_UBAHN=3
MOD_BUS=5

@app.task(bind=True)
def get_json(args):
    request_json = requests.get('http://m.vvs.de/VELOC')
    json = request_json.json()
    keys = yamjam("keys.yaml")
    auth = tweepy.OAuthHandler(keys['twitter']['rbahn']['consumer_key'], keys['twitter']['rbahn']['consumer_secret'])
    auth.set_access_token(keys['twitter']['rbahn']['access_token'], keys['twitter']['rbahn']['access_token_secret'])
    api_rbahn = tweepy.API(auth)
    auth = tweepy.OAuthHandler(keys['twitter']['sbahn']['consumer_key'], keys['twitter']['sbahn']['consumer_secret'])
    auth.set_access_token(keys['twitter']['sbahn']['access_token'], keys['twitter']['sbahn']['access_token_secret'])
    api_sbahn = tweepy.API(auth)
    auth = tweepy.OAuthHandler(keys['twitter']['ubahn']['consumer_key'], keys['twitter']['ubahn']['consumer_secret'])
    auth.set_access_token(keys['twitter']['ubahn']['access_token'], keys['twitter']['ubahn']['access_token_secret'])
    api_ubahn = tweepy.API(auth)
    auth = tweepy.OAuthHandler(keys['twitter']['bus']['consumer_key'], keys['twitter']['bus']['consumer_secret'])
    auth.set_access_token(keys['twitter']['bus']['access_token'], keys['twitter']['bus']['access_token_secret'])
    api_bus = tweepy.API(auth)
    redis_connection = redis.StrictRedis(host='localhost', port=6379, db=1)

    for entry in json:
        timestamp_before = unix_timestamp_to_datetime(entry.get("TimestampBefore")[6:16])

        day_of_operation = unix_timestamp_to_datetime(entry.get("DayOfOperation")[6:16])
        timestamp = unix_timestamp_to_datetime(entry.get("Timestamp")[6:16])
        vvs_id = entry.get("ID")

        line_text = entry.get("LineText")
        longitude = entry.get("Longitude")
        longitude_before = entry.get("LongitudeBefore", "0")
        latitude = entry.get("Latitude")
        latitude_before = entry.get("LatitudeBefore", "0")
        if latitude_before is None:
            latitude_before = 0
        if longitude_before is None:
            longitude_before = 0
        is_at_stop = entry.get("IsAtStop")
        journey_id = entry.get("JourneyIdentifier")
        delay = entry.get("Delay")

        product_id = entry.get("ProductIdentifier")
        mod_code = entry.get("ModCode")
        real_time_available = entry.get("RealtimeAvailable")


        operator = entry.get("Operator")
        try:
            direction, created = Direction.objects.get_or_create(name=entry.get("DirectionText").encode('iso-8859-1').decode('utf-8'))
        except IntegrityError:
            pass
        try:
            current_stop, created = Stop.objects.get_or_create(vvs_id=entry.get("CurrentStop").split("#")[0])
        except IntegrityError:
            pass
        try:
            if entry.get("NextStop").split("#")[0]:
                next_stop, created = Stop.objects.get_or_create(vvs_id=entry.get("NextStop").split("#")[0])
            else:
                next_stop = current_stop
        except IntegrityError:
            pass

        try:
            line, created = Line.objects.get_or_create(line_text=line_text)
        except IntegrityError:
            pass

        if not is_at_stop:
            is_at_stop = False
        else:
            is_at_stop = True

        transport, created = VVSTransport.objects.get_or_create(line=line,
                                                       direction=direction,
                                                       journey_id=journey_id,
                                                       operator=operator,
                                                       mod_code=mod_code,
                                                       product_id=product_id)
        journey, created = VVSJourney.objects.get_or_create(vvs_transport=transport,
                                                   day_of_operation=day_of_operation,
                                                   vvs_id=vvs_id)
        if journey.vvs_id not in cache and delay >= 10*60:
            print(journey.vvs_id)
            time_string = str(datetime.timedelta(seconds=delay))
            text = "{} Richtung {} mit der nächsten Haltestelle {} hat {} Verspätung".format(line.line_text,
                                                                                             direction.name,
                                                                                             next_stop.name,
                                                                                             str(time_string))
            json_text ="{{\"delay\":\"{}\", \"line\":\"{}\",\"direction\":\"{}\",\"next_stop\":\"{}\"}}".format(str(time_string),
                                                                                             line.line_text,
                                                                                             direction.name,
                                                                                             next_stop.name)
            print(json_text)
            if not redis_connection.exists(journey.vvs_id):
                redis_connection.set(journey.vvs_id, json_text, 60*60)
                keys = redis_connection.keys("*")
                print("redis")
                if len(keys) > 20:
                    time_to_live = []
                    for key in keys:
                        time_to_live.append((key, redis_connection.ttl(key)))
                    sorted(time_to_live, key=itemgetter(1))
                    print(time_to_live)
                    to_delete = time_to_live[0:len(time_to_live)-20]
                    for key in to_delete:
                        redis_connection.delete(key)




            cache.set(journey.vvs_id, delay, 60*60) # 60 Minute timeout

            if mod_code == MOD_RBAHN:
                api = api_rbahn
            elif mod_code == MOD_SBAHN:
                api = api_sbahn
            elif mod_code == MOD_UBAHN:
                api = api_ubahn
            elif mod_code == MOD_BUS:
                api = api_bus
            try:
                api.update_status(text)
            except tweepy.error.TweepError as e:
                print(e)
            
            print("{} Richtung {} mit der nächsten Haltestelle {} hat {}s Verspätung".format(line.line_text, direction.name, next_stop.name, str(time_string)))

        if delay == 0 and journey.vvs_id in cache:
            cache.delete(journey.vvs_id)

        VVSData.objects.create(vvs_journey=journey,
                               timestamp=timestamp,
                               timestamp_before=timestamp_before,
                               coordinates_before=Point(float(longitude_before), float(latitude_before)),
                               coordinates=Point(float(longitude), float(latitude)),
                               delay=delay,
                               current_stop=current_stop,
                               next_stop=next_stop,
                               real_time_available=real_time_available,
                               is_at_stop=is_at_stop)


def unix_timestamp_to_datetime(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp)).replace(tzinfo=UTC)

@app.task(bind=True)
def crawl_stop_names(args):
    url = "http://m.vvs.de/jqm/controller/XSLT_COORD_REQUEST?&coord=3511295%3A755934%3ANBWT&inclFilter=1&language=en&outputFormat=json&type_1=STOP&radius_1=900000000&coordOutputFormat=WGS84[DD.ddddd]"
    response = requests.get(url)
    response_json = response.json()
    for pin in response_json.get('pins'):
        if pin.get('type') == "STOP":
            try:
                stop = Stop.objects.get(vvs_id=int(pin.get('id')))
                stop.name = pin.get('desc').encode('iso-8859-1').decode('utf-8')
                stop.locality = pin.get('locality').encode('iso-8859-1').decode('utf-8')
                longitude, latitude = pin.get('coords').split(',')
                stop.coordinates = Point(float(longitude),float(latitude))
                stop.save()
            except Stop.DoesNotExist:

                pass
            except IntegrityError:
                pass


def get_max_delays_today():
    keys = yamjam("keys.yaml")
    midnight = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    top_3_delays = VVSJourney.objects.filter(day_of_operation__gte=midnight).annotate(max_delay=Max('vvsdata__delay')).order_by('-max_delay')[:3]
    top_3_text = []
    for candidate in top_3_delays:
        top_3_text.append("{}, {}s".format(candidate.vvs_transport.line.line_text, candidate.max_delay))

    text = "Top 3 Verspätungen: {}".format(",".join(top_3_text))
    auth = tweepy.OAuthHandler(keys['twitter']['sbahn']['consumer_key'], keys['twitter']['sbahn']['consumer_secret'])
    auth.set_access_token(keys['twitter']['sbahn']['access_token'], keys['twitter']['sbahn']['access_token_secret'])
    api = tweepy.API(auth)
    try:
        api.update_status(text)
    except tweepy.error.TweepError as e:
        print(e)


