from .models import Accident
import django_filters


class AccidentFilter(django_filters.FilterSet):
    data_time = django_filters.NumberFilter(field_name='data_time', lookup_expr='year')
    data_time__gte = django_filters.NumberFilter(field_name='data_time', lookup_expr='year__gte')
    data_time__lte = django_filters.NumberFilter(field_name='data_time', lookup_expr='year__lte')

    class Meta:
        model = Accident
        fields = [
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
            "num_of_accidents",
            "num_of_fatalities",
            "num_of_injured",
            "is_offender_intoxicated",
        ]
