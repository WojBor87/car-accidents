from django.db import models


# Create your models here.
class RoadCategory(models.Model):
    name = models.CharField(max_length=30)


class Road(models.Model):
    name = models.CharField(max_length=15)
    road_category_id = models.ForeignKey(RoadCategory, on_delete=models.CASCADE)


class Voivodeship(models.Model):
    name = models.CharField(max_length=20)


class District(models.Model):
    name = models.CharField(max_length=15)
    voivodeship_id = models.ForeignKey(Voivodeship, on_delete=models.CASCADE)


class Town(models.Model):
    name = models.CharField(max_length=35)
    district_id = models.ForeignKey(District, on_delete=models.CASCADE)
    is_city = models.BooleanField()


class RoadGeometry(models.Model):
    name = models.IntegerField()


class PlaceOfTheEvent(models.Model):
    name = models.CharField(max_length=70)


class TypeOfInjury(models.Model):
    name = models.CharField(max_length=40)


class TypeOfAccident(models.Model):
    name = models.CharField(max_length=50)


class Lighting(models.Model):
    name = models.CharField(max_length=40)


class WeatherConditions(models.Model):
    name = models.CharField(max_length=50)


class PedestrianBehavior(models.Model):
    name = models.CharField(max_length=50)


class DriverBehavior(models.Model):
    name = models.CharField(max_length=50)


class Notes(models.Model):
    name = models.CharField(max_length=255)


class Accident(models.Model):
    data_time = models.DateTimeField()
    location_id = models.ForeignKey(Town, on_delete=models.CASCADE)
    road_id = models.ForeignKey(Road, on_delete=models.CASCADE)
    is_built_up_area = models.BooleanField()
    longitude = models.FloatField()
    latitude = models.FloatField()
    road_geometry_id = models.ForeignKey(RoadGeometry, on_delete=models.CASCADE)
    place_of_the_event_id = models.ForeignKey(PlaceOfTheEvent, on_delete=models.CASCADE)
    weather_conditions_id = models.ForeignKey(WeatherConditions, on_delete=models.CASCADE)
    lighting_id = models.ForeignKey(Lighting, on_delete=models.CASCADE)
    type_of_accident_id = models.ForeignKey(TypeOfAccident, on_delete=models.CASCADE)
    num_of_accidents = models.IntegerField()
    num_of_fatalities = models.IntegerField()
    num_of_injured = models.IntegerField()
    type_of_injury_id = models.ForeignKey(TypeOfInjury, on_delete=models.CASCADE)
    is_offender_intoxicated = models.BooleanField()
    driver_behavior = models.ForeignKey(DriverBehavior, on_delete=models.CASCADE)
    pedestrian_behavior = models.ForeignKey(PedestrianBehavior, on_delete=models.CASCADE)
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE)
