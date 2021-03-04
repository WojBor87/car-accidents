from django.db import models


# Create your models here.
class District(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class DistrictCommune(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class CharPlaceOfTheEvent(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class WeatherConditions(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Lighting(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class RoadCategory(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class TypeOfRoad(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Road(models.Model):
    read_number = models.CharField(max_length=255)
    road_category = models.OneToOneField(RoadCategory, on_delete=models.CASCADE)
    type_of_road = models.OneToOneField(TypeOfRoad, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.road_category}"


class RoadGeometry(models.Model):
    name = models.IntegerField

    def __str__(self):
        return f"{self.name}"


class Area(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class TypeOfAccident(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class TypeOfInjury(models.Model):
    pass


class Accident(models.Model):
    pass
