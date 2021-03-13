from .models import Accident
import django_filters


class AccidentFilter(django_filters.FilterSet):
    class Meta:
        model = Accident
        fields =['idksip']
