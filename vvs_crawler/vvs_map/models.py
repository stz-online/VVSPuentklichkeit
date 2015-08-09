from django.db import models

# Create your models here.


class VVSTransport(models.Model):
    direction_text = models.CharField(max_length=300)
    line_text = models.CharField(max_length=300)
    journey_id = models.IntegerField()
    operator = models.TextField()
    mod_code = models.IntegerField()
    product_id = models.CharField(max_length=300)

    class Meta:
        unique_together = ("direction_text", "line_text", "journey_id")

    def __str__(self):
        return "Linie {}, Richtung {}, Journey_id {}".format(self.line_text, self.direction_text, self.journey_id)


class VVSJourney(models.Model):
    vvs_transport = models.ForeignKey("vvs_map.VVSTransport")
    day_of_operation = models.DateTimeField()
    vvs_id = models.IntegerField()


class VVSData(models.Model):
    vvs_journey = models.ForeignKey("VVSJourney")
    timestamp = models.DateTimeField()
    timestamp_before = models.DateTimeField()
    longitude = models.IntegerField()
    longitude_before = models.IntegerField(null=True, blank=True)
    latitude = models.IntegerField()
    latitude_before = models.IntegerField(null=True, blank=True)
    delay = models.IntegerField()
    is_at_stop = models.BooleanField()
    current_stop = models.CharField(max_length=300)
    next_stop = models.CharField(max_length=300)
    real_time_available = models.BooleanField()