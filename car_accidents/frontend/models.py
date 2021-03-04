from django.db import models


# Create your models here.
class Accident(models.Model):
    pass


class District(models.Model):
    pass


class DistrictCommune(models.Model):
    pass


class CharPlaceOfTheEvent(models.Model):
    pass


class WeatherConditions(models.Model):
    pass


class Lighting(models.Model):
    pass


class Road(models.Model):
    pass


class RoadCategory(models.Model):
    pass


class TypeOfRoad(models.Model):
    pass


class RoadGeometry(models.Model):
    pass


class Area(models.Model):
    pass


class TypeOfAccident(models.Model):
    name


class TypeOfInjury(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"
