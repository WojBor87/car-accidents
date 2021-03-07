from django.shortcuts import render, HttpResponse
from django.db import connection
import pandas as pd
from pathlib import Path
from django.views.generic.list import ListView

from .models import (
    Accident,
    District,
    DriverBehavior,
    Lighting,
    Notes,
    PedestrianBehavior,
    PlaceOfTheEvent,
    Road,
    RoadCategory,
    RoadGeometry,
    Town,
    TypeOfAccident,
    TypeOfInjury,
    Voivodeship,
    WeatherConditions,
)


# Create your views here.
def filters_form(request):
    db_name = connection.settings_dict['NAME']
    return render(request, 'frontend/filters_form.html', {'db_name': db_name})


def import_csv(request, file_name):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    df = pd.read_csv('frontend/static/frontend/csv' / Path(file_name))
    return HttpResponse(df.to_html())
    # return render(request, 'frontend/import_csv.html', {'csv_df': df.to_html()})


class AccidentView(ListView):
    model = Accident


        # data_names = {
    #     "district": District,
    #     "driver_behavior": DriverBehavior,
    #     "lighting": Lighting,
    #     "notes": Notes,
    #     "pedestrian_behavior": PedestrianBehavior,
    #     "place_of_the_event": PlaceOfTheEvent,
    #     "road": Road,
    #     "road_category": RoadCategory,
    #     "road_geometry": RoadGeometry,
    #     "town": Town,
    #     "type_of_accident": TypeOfAccident,
    #     "type_of_injury": TypeOfInjury,
    #     "voivodeship": Voivodeship,
    #     "weather_conditions": WeatherConditions,
    #     "is_built_up_area": Accident.is_built_up_area,
    #     "data_time": Accident.data_time,
    #     "num_of_accidents": Accident.num_of_accidents,
    #     "num_of_fatalities": Accident.num_of_fatalities,
    #     "num_of_injured": Accident.num_of_injured,
    #     "is_offender_intoxicated": Accident.is_offender_intoxicated,
    # }
    #
    # def get_request_data(self, request):
    #     if request.method == "GET":
    #         district = request.GET.get("district")
    #         driver_behavior = request.GET.get("driver_behavior")
    #         lighting = request.GET.get("lighting")
    #         notes = request.GET.get("notes")
    #         pedestrian_behavior = request.GET.get("pedestrian_behavior")
    #         place_of_the_event = request.GET.get("place_of_the_event")
    #         road = request.GET.get("road")
    #         road_category = request.GET.get("road_category")
    #         road_geometry = request.GET.get("road_geometry")
    #         town = request.GET.get("town")
    #         type_of_accident = request.GET.get("type_of_accident")
    #         type_of_injury = request.GET.get("type_of_injury")
    #         voivodeship = request.GET.get("voivodeship")
    #         weather_conditions = request.GET.get("weather_conditions")
    #         is_built_up_area = request.GET.get("is_built_up_area")
    #         data_time = request.GET.get("data_time")
    #         num_of_accidents = request.GET.get("num_of_accidents")
    #         num_of_fatalities = request.GET.get("num_of_fatalities")
    #         num_of_injured = request.GET.get("num_of_injured")
    #         is_offender_intoxicated = request.GET.get("is_offender_intoxicated")
    #         return [
    #             district,
    #             driver_behavior,
    #             lighting,
    #             notes,
    #             pedestrian_behavior,
    #             place_of_the_event,
    #             road,
    #             road_category,
    #             road_geometry,
    #             town,
    #             type_of_accident,
    #             type_of_injury,
    #             voivodeship,
    #             weather_conditions,
    #             is_built_up_area,
    #             data_time,
    #             num_of_accidents,
    #             num_of_fatalities,
    #             num_of_injured,
    #             is_offender_intoxicated,
    #         ]
    #     else:
    #         return []
    #
    # def collect_data_from_db(self, request):
    #     post_data = self.get_request_data(request)
    #     post_collected_data = []
    #     for data in post_data:
    #         if data:
    #             data = self.data_names[data].objects.get(data)
    #         else:
    #             data = self.data_names[data].objects.all()
    #         post_collected_data.append(data)
    #     return post_collected_data
    #
    # def create_view(self, request):
    #     data = self.collect_data_from_db(request)
    #     result_filter = {}
    #     for current_filter in data:
    #         result_filter[current_filter] = current_filter
    #
    #     return render(
    #         request,
    #         'fronted/filter_test.html',
    #         {
    #             "district": result_filter["district"],
    #             "driver_behavior": result_filter["driver_behavior"],
    #             "lighting": result_filter["lighting"],
    #             "notes": result_filter["notes"],
    #             "pedestrian_behavior": result_filter["pedestrian_behavior"],
    #             "place_of_the_event": result_filter["place_of_the_event"],
    #             "road": result_filter["road"],
    #             "road_category": result_filter["road_category"],
    #             "road_geometry": result_filter["road_geometry"],
    #             "town": result_filter["town"],
    #             "type_of_accident": result_filter["type_of_accident"],
    #             "type_of_injury": result_filter["type_of_injury"],
    #             "voivodeship": result_filter["voivodeship"],
    #             "weather_conditions": result_filter["weather_conditions"],
    #             "is_built_up_area": result_filter["is_built_up_area"],
    #             "data_time": result_filter["data_time"],
    #             "num_of_accidents": result_filter["num_of_accidents"],
    #             "num_of_fatalities": result_filter["num_of_fatalities"],
    #             "num_of_injured": result_filter["num_of_injured"],
    #             "is_offender_intoxicated": result_filter["is_offender_intoxicated"],
    #         }
    #     )
