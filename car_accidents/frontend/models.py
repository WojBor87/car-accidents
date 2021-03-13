from django.db import models


# Create your models here.
class RoadCategory(models.Model):
    name = models.CharField(max_length=30, verbose_name="RoadCategory name")

    def __str__(self):
        return self.name

class Road(models.Model):
    name = models.CharField(max_length=15, verbose_name="Road name", primary_key=True)
    road_category_id = models.ForeignKey(
        RoadCategory,
        on_delete=models.CASCADE,
        verbose_name="Road road_category_id",
        blank=True,
        null=True,
        default=None,
    )

    def __str__(self):
        return self.name



class Voivodeship(models.Model):
    name = models.CharField(max_length=20, verbose_name="Voivodeship name")

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=15, verbose_name="District name")
    # todo: should be not nullable. find out based on longitude and latitude or district
    voivodeship_id = models.ForeignKey(
        Voivodeship,
        on_delete=models.CASCADE,
        verbose_name="District voivodeship_id",
        blank=True,
        null=True,
        default=None,
    )

    def __str__(self):
        return self.name

class Town(models.Model):
    name = models.CharField(max_length=35, verbose_name="Town name")
    district_id = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name="Town district_id")
    is_city = models.BooleanField(verbose_name="Town is_city")

    def __str__(self):
        return self.name

class RoadGeometry(models.Model):
    name = models.CharField(max_length=35, verbose_name="RoadGeometry name")

    def __str__(self):
        return self.name

class PlaceOfTheEvent(models.Model):
    name = models.CharField(max_length=70, verbose_name="PlaceOfTheEvent name")

    def __str__(self):
        return self.name

class TypeOfInjury(models.Model):
    name = models.CharField(max_length=40, verbose_name="TypeOfInjury name")

    def __str__(self):
        return self.name

class TypeOfAccident(models.Model):
    name = models.CharField(max_length=50, verbose_name="TypeOfAccident name")

    def __str__(self):
        return self.name

class Lighting(models.Model):
    name = models.CharField(max_length=40, verbose_name="Lighting name")

    def __str__(self):
        return self.name

class WeatherConditions(models.Model):
    name = models.CharField(max_length=50, verbose_name="WeatherConditions name")

    def __str__(self):
        return self.name

class PedestrianBehavior(models.Model):
    name = models.CharField(max_length=150, verbose_name="PedestrianBehavior name")

    def __str__(self):
        return self.name

class DriverBehavior(models.Model):
    name = models.CharField(max_length=100, verbose_name="DriverBehavior name")

    def __str__(self):
        return self.name

class Notes(models.Model):
    name = models.CharField(max_length=255, verbose_name="Notes name")

    def __str__(self):
        return self.name

class Accident(models.Model):
    idksip = models.CharField(max_length=15, primary_key=True, verbose_name="Accident unique idksip key")
    data_time = models.DateTimeField(verbose_name="Date")
    town_name = models.ForeignKey(Town, on_delete=models.CASCADE, verbose_name="Town")
    road = models.ForeignKey(
        Road, on_delete=models.CASCADE, verbose_name="Road number", blank=True, null=True, default=None
    )
    is_built_up_area = models.BooleanField(verbose_name="built-up area")
    longitude = models.FloatField(verbose_name="Longitude")
    latitude = models.FloatField(verbose_name="Latitude")
    road_geometry = models.ForeignKey(
        RoadGeometry,
        on_delete=models.CASCADE,
        verbose_name="Road geometry",
        blank=True,
        null=True,
        default=None,
    )
    place_of_the_event = models.ForeignKey(
        PlaceOfTheEvent, on_delete=models.CASCADE, verbose_name="Place of the event"
    )
    weather_conditions = models.ForeignKey(
        WeatherConditions, on_delete=models.CASCADE, verbose_name="Weather Conditions"
    )
    lighting = models.ForeignKey(Lighting, on_delete=models.CASCADE, verbose_name="Lighting")
    type_of_accident = models.ForeignKey(
        TypeOfAccident, on_delete=models.CASCADE, verbose_name="Type of accident"
    )
    num_of_accidents = models.IntegerField(verbose_name="Number of accidents")
    num_of_fatalities = models.IntegerField(verbose_name="Number of fatalities")
    num_of_injured = models.IntegerField(verbose_name="Number of injured")
    type_of_injury = models.ForeignKey(
        TypeOfInjury,
        on_delete=models.CASCADE,
        verbose_name="Type of injury",
        blank=True,
        null=True,
        default=None,
    )
    is_offender_intoxicated = models.BooleanField(verbose_name="Is offender intoxicated?")
    driver_behavior = models.ForeignKey(
        DriverBehavior,
        on_delete=models.CASCADE,
        verbose_name="Driver behavior",
        blank=True,
        null=True,
        default=None,
    )
    pedestrian_behavior = models.ForeignKey(
        PedestrianBehavior,
        on_delete=models.CASCADE,
        verbose_name="Pedestrian behavior",
        blank=True,
        null=True,
        default=None,
    )
    notes = models.ForeignKey(
        Notes, on_delete=models.CASCADE, verbose_name="Notes", blank=True, null=True, default=None
    )

    def __str__(self):
        return self.name