from django.contrib.gis.db import models

# Create your models here.
class Line(models.Model):
    line_text = models.CharField(max_length=300, unique=True)


class VVSTransport(models.Model):
    line = models.ForeignKey('vvs_map.Line')
    direction = models.ForeignKey('vvs_map.Direction')
    journey_id = models.IntegerField()
    operator = models.TextField()
    mod_code = models.IntegerField()
    product_id = models.CharField(max_length=300)

    class Meta:
        unique_together = ("direction", "line", "journey_id")

    def __str__(self):
        return "Linie {}, Richtung {}, Journey_id {}".format(self.line, self.direction, self.journey_id)


class VVSJourney(models.Model):
    vvs_transport = models.ForeignKey("vvs_map.VVSTransport")
    day_of_operation = models.DateTimeField()
    vvs_id = models.IntegerField(unique=True)

class Stop(models.Model):
    vvs_id = models.CharField(max_length=300)
    name = models.CharField(max_length=300, unique=True)
    coordinates = models.PointField(null=True, blank=True)
    locality = models.CharField(max_length=300)




    def __str__(self):
        return "{}-{}".format(self.locality, self.name)

class VVSData(models.Model):
    vvs_journey = models.ForeignKey("vvs_map.VVSJourney")
    timestamp = models.DateTimeField()
    timestamp_before = models.DateTimeField()
    coordinates_before = models.PointField(help_text="Represented as (longitude, latitude)", null=True)
    coordinates = models.PointField(help_text="Represented as (longitude, latitude)")
    delay = models.IntegerField()
    is_at_stop = models.BooleanField()
    current_stop = models.ForeignKey('vvs_map.Stop', related_name="current_stop")
    next_stop = models.ForeignKey('vvs_map.Stop', related_name="next_stop")
    real_time_available = models.BooleanField()


class Direction(models.Model):
    name = models.CharField(max_length=300)
