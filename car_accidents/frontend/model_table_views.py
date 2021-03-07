from django_tables2 import SingleTableView
from frontend.models import (
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
from frontend.tables import (
    RoadCategoryTable,
    RoadTable,
    VoivodeshipTable,
    DistrictTable,
    TownTable,
    RoadGeometryTable,
    PlaceOfTheEventTable,
    TypeOfInjuryTable,
    TypeOfAccidentTable,
    LightingTable,
    WeatherConditionsTable,
    PedestrianBehaviorTable,
    DriverBehaviorTable,
    NotesTable,
    AccidentTable,
)


class RoadCategoryListView(SingleTableView):
    model = RoadCategory
    table_class = RoadCategoryTable
    template_name = 'frontend/helpers/table_print_model.html'


class RoadListView(SingleTableView):
    model = Road
    table_class = RoadTable
    template_name = 'frontend/helpers/table_print_model.html'


class VoivodeshipListView(SingleTableView):
    model = Voivodeship
    table_class = VoivodeshipTable
    template_name = 'frontend/helpers/table_print_model.html'


class DistrictListView(SingleTableView):
    model = District
    table_class = DistrictTable
    template_name = 'frontend/helpers/table_print_model.html'


class TownListView(SingleTableView):
    model = Town
    table_class = TownTable
    template_name = 'frontend/helpers/table_print_model.html'


class RoadGeometryListView(SingleTableView):
    model = RoadGeometry
    table_class = RoadGeometryTable
    template_name = 'frontend/helpers/table_print_model.html'


class PlaceOfTheEventListView(SingleTableView):
    model = PlaceOfTheEvent
    table_class = PlaceOfTheEventTable
    template_name = 'frontend/helpers/table_print_model.html'


class TypeOfInjuryListView(SingleTableView):
    model = TypeOfInjury
    table_class = TypeOfInjuryTable
    template_name = 'frontend/helpers/table_print_model.html'


class TypeOfAccidentListView(SingleTableView):
    model = TypeOfAccident
    table_class = TypeOfAccidentTable
    template_name = 'frontend/helpers/table_print_model.html'


class LightingListView(SingleTableView):
    model = Lighting
    table_class = LightingTable
    template_name = 'frontend/helpers/table_print_model.html'


class WeatherConditionsListView(SingleTableView):
    model = WeatherConditions
    table_class = WeatherConditionsTable
    template_name = 'frontend/helpers/table_print_model.html'


class PedestrianBehaviorListView(SingleTableView):
    model = PedestrianBehavior
    table_class = PedestrianBehaviorTable
    template_name = 'frontend/helpers/table_print_model.html'


class DriverBehaviorListView(SingleTableView):
    model = DriverBehavior
    table_class = DriverBehaviorTable
    template_name = 'frontend/helpers/table_print_model.html'


class NotesListView(SingleTableView):
    model = Notes
    table_class = NotesTable
    template_name = 'frontend/helpers/table_print_model.html'


class AccidentListView(SingleTableView):
    model = Accident
    table_class = AccidentTable
    template_name = 'frontend/helpers/table_print_model.html'
