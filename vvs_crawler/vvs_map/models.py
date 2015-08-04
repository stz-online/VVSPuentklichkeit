from django.db import models

# Create your models here.

class MapEntry(models.Model):
    created = models.DateTimeField(auto_created=True, auto_now=True)
    timestamp_before = models.DateTimeField()
    vvs_id = models.IntegerField()
    direction_text = models.TextField()
    line_text = models.TextField()
    longitude = models.IntegerField()
    latitude_before = models.IntegerField(null=True, blank=True)
    is_at_stop = models.BooleanField()
    timestamp = models.DateTimeField()
    journey_id = models.IntegerField()
    delay = models.IntegerField()
    current_stop = models.CharField(max_length=300)
    product_id = models.CharField(max_length=300)
    mod_code = models.IntegerField()
    real_time_available = models.BooleanField()
    longitude_before = models.IntegerField(null=True, blank=True)
    day_of_operation = models.DateTimeField()
    operator = models.TextField()
    latitude = models.IntegerField()
    next_stop = models.CharField(max_length=300)