from django.db import models


# Create your models here.
class RoadCategory(models.Model):
    name = models.CharField(max_length=30, verbose_name="RoadCategory name")


class Road(models.Model):
    name = models.CharField(max_length=15, verbose_name="Road name")
    road_category_id = models.ForeignKey(RoadCategory, on_delete=models.CASCADE, verbose_name="Road road_category_id")


class Voivodeship(models.Model):
    name = models.CharField(max_length=20, verbose_name="Voivodeship name")


class District(models.Model):
    name = models.CharField(max_length=15, verbose_name="District name")
    voivodeship_id = models.ForeignKey(Voivodeship, on_delete=models.CASCADE, verbose_name="District voivodeship_id")


class Town(models.Model):
    name = models.CharField(max_length=35, verbose_name="Town name")
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Town district_id")
    is_city = models.BooleanField(verbose_name="Town is_city")


class RoadGeometry(models.Model):
    name = models.IntegerField(verbose_name="RoadGeometry name")


class PlaceOfTheEvent(models.Model):
    name = models.CharField(max_length=70, verbose_name="PlaceOfTheEvent name")


class TypeOfInjury(models.Model):
    name = models.CharField(max_length=40, verbose_name="TypeOfInjury name")


class TypeOfAccident(models.Model):
    name = models.CharField(max_length=50, verbose_name="TypeOfAccident name")


class Lighting(models.Model):
    name = models.CharField(max_length=40, verbose_name="Lighting name")


class WeatherConditions(models.Model):
    name = models.CharField(max_length=50, verbose_name="WeatherConditions name")


class PedestrianBehavior(models.Model):
    name = models.CharField(max_length=50, verbose_name="PedestrianBehavior name")


class DriverBehavior(models.Model):
    name = models.CharField(max_length=50, verbose_name="DriverBehavior name")


class Notes(models.Model):
    name = models.CharField(max_length=255, verbose_name="Notes name")


class Accident(models.Model):
    data_time = models.DateTimeField(verbose_name="Accident data_time")
    town_name = models.ForeignKey(Town, on_delete=models.CASCADE, verbose_name="Accident town_name")
    road_id = models.ForeignKey(Road, on_delete=models.CASCADE, verbose_name="Accident road_id")
    is_built_up_area = models.BooleanField(verbose_name="Accident is_built_up_area")
    longitude = models.FloatField(verbose_name="Accident longitude")
    latitude = models.FloatField(verbose_name="Accident latitude")
    road_geometry_id = models.ForeignKey(
        RoadGeometry, on_delete=models.CASCADE, verbose_name="Accident road_geometry_id"
    )
    place_of_the_event_id = models.ForeignKey(
        PlaceOfTheEvent, on_delete=models.CASCADE, verbose_name="Accident place_of_the_event_id"
    )
    weather_conditions_id = models.ForeignKey(
        WeatherConditions, on_delete=models.CASCADE, verbose_name="Accident weather_conditions_id"
    )
    lighting_id = models.ForeignKey(Lighting, on_delete=models.CASCADE, verbose_name="Accident lighting_id")
    type_of_accident_id = models.ForeignKey(
        TypeOfAccident, on_delete=models.CASCADE, verbose_name="Accident type_of_accident_id"
    )
    num_of_accidents = models.IntegerField(verbose_name="Accident num_of_accidents")
    num_of_fatalities = models.IntegerField(verbose_name="Accident num_of_fatalities")
    num_of_injured = models.IntegerField(verbose_name="Accident num_of_injured")
    type_of_injury_id = models.ForeignKey(
        TypeOfInjury, on_delete=models.CASCADE, verbose_name="Accident type_of_injury_id"
    )
    is_offender_intoxicated = models.BooleanField(verbose_name="Accident is_offender_intoxicated")
    driver_behavior = models.ForeignKey(
        DriverBehavior, on_delete=models.CASCADE, verbose_name="Accident driver_behavior"
    )
    pedestrian_behavior = models.ForeignKey(
        PedestrianBehavior, on_delete=models.CASCADE, verbose_name="Accident pedestrian_behavior"
    )
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE, verbose_name="Accident notes")
