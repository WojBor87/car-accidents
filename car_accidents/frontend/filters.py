from .models import Accident
import django_filters


class AccidentFilter(django_filters.FilterSet):
    class Meta:
        model = Accident
        fields =[
            'driver_behavior',
            'lighting',
            'pedestrian_behavior',
            'place_of_the_event',
            'road',
            'road_geometry',
            'town_name',
            'type_of_accident',
            'type_of_injury',
            'weather_conditions',
            "is_built_up_area",
            "data_time",
            "num_of_accidents",
            "num_of_fatalities",
            "num_of_injured",
            "is_offender_intoxicated",
        ]
