import django_tables2 as tables
from .models import (
    RoadCategory,
    Road,
    Voivodeship,
    District,
    Town,
    RoadGeometry,
    PlaceOfTheEvent,
    TypeOfInjury,
    TypeOfAccident,
    Lighting,
    WeatherConditions,
    PedestrianBehavior,
    DriverBehavior,
    Notes,
    Accident,
)


class RoadCategoryTable(tables.Table):
    class Meta:
        model = RoadCategory
        template_name = "django_tables2/bootstrap.html"


class RoadTable(tables.Table):
    class Meta:
        model = Road
        template_name = "django_tables2/bootstrap.html"


class VoivodeshipTable(tables.Table):
    class Meta:
        model = Voivodeship
        template_name = "django_tables2/bootstrap.html"


class DistrictTable(tables.Table):
    class Meta:
        model = District
        template_name = "django_tables2/bootstrap.html"


class TownTable(tables.Table):
    class Meta:
        model = Town
        template_name = "django_tables2/bootstrap.html"


class RoadGeometryTable(tables.Table):
    class Meta:
        model = RoadGeometry
        template_name = "django_tables2/bootstrap.html"


class PlaceOfTheEventTable(tables.Table):
    class Meta:
        model = PlaceOfTheEvent
        template_name = "django_tables2/bootstrap.html"


class TypeOfInjuryTable(tables.Table):
    class Meta:
        model = TypeOfInjury
        template_name = "django_tables2/bootstrap.html"


class TypeOfAccidentTable(tables.Table):
    class Meta:
        model = TypeOfAccident
        template_name = "django_tables2/bootstrap.html"


class LightingTable(tables.Table):
    class Meta:
        model = Lighting
        template_name = "django_tables2/bootstrap.html"


class WeatherConditionsTable(tables.Table):
    class Meta:
        model = WeatherConditions
        template_name = "django_tables2/bootstrap.html"


class PedestrianBehaviorTable(tables.Table):
    class Meta:
        model = PedestrianBehavior
        template_name = "django_tables2/bootstrap.html"


class DriverBehaviorTable(tables.Table):
    class Meta:
        model = DriverBehavior
        template_name = "django_tables2/bootstrap.html"


class NotesTable(tables.Table):
    class Meta:
        model = Notes
        template_name = "django_tables2/bootstrap.html"


class AccidentTable(tables.Table):
    class Meta:
        model = Accident
        template_name = "django_tables2/bootstrap.html"
