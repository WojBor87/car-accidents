from django.shortcuts import render, HttpResponse
from django.views.generic import View, ListView
from django.db import connection
import pandas as pd
import numpy as np
from pathlib import Path
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


# Create your views here.
def filters_form(request):
    db_name = connection.settings_dict['NAME']
    return render(request, 'frontend/filters_form.html', {'db_name': db_name})


class ImportCsvView(View):
    def get(self, request, file_name):
        pd.set_option('display.max_columns', None)
        self.df = pd.read_csv('frontend/static/frontend/csv' / Path(file_name))

        self.process_behavior() if 'driver behavior' in self.df else self.process_all()
        table_changes = (
            self.insert_or_replace_behavior() if 'driver behavior' in self.df else self.insert_or_replace_all()
        )

        return render(request, 'frontend/import_csv.html', {'table_changes': table_changes})

    def process_all(self):
        self.df['road_category'].replace('Nieokreślone (puste pole)', np.nan, inplace=True)
        self.df['road_number'].replace('0', np.nan, inplace=True)
        self.df['district'] = self.df['district'].str.replace('POWIAT ', '')
        self.df[['town', 'is_city']] = self.df['district_commune'].str.split('-', 1, expand=True)
        self.df['town'].apply(str.strip)
        booleanDictionary = {' OBSZAR MIEJSKI': True, ' OBSZAR WIEJSKI': False}
        self.df['is_city'] = self.df['is_city'].map(booleanDictionary)
        self.df['road_geometry'].replace('0', np.nan, inplace=True)
        booleanDictionary = {'Obszar zabudowany': True, 'Obszar niezabudowany': False}
        self.df['area'] = self.df['area'].map(booleanDictionary)
        self.df['Longitude'].apply(float)
        self.df['Latitude'].apply(float)
        self.df['num_of_accidents'].apply(int)
        self.df['num_of_fatalities'].apply(int)
        self.df['num_of_injured'].apply(int)
        self.df['type_of_injury'].replace('Nieokreślone (puste pole)', np.nan, inplace=True)
        booleanDictionary = {'T': True, 'N': False}
        self.df['is_offender_intoxicated'] = self.df['is_offender_intoxicated'].map(booleanDictionary)
        

    def process_behavior(self):
        self.df['driver behavior'].replace('', np.nan, inplace=True)
        self.df['pedestrian behavior'].replace('', np.nan, inplace=True)
        self.df['other'].replace('', np.nan, inplace=True)
        

    def insert_or_replace_all(self):
        for i, *fields in self.df.itertuples():
            fields = dict(zip(self.df.columns, fields))
            if not Accident.objects.filter(idksip=fields['IDKSIP']).exists():
                print(f"{i}: {fields['area']}")

    def insert_or_replace_behavior(self):
        for i, *fields in self.df.itertuples():
            fields = dict(zip(self.df.columns, fields))
            if Accident.objects.filter(idksip=fields['IDKSIP']).exists():
                print(fields)
                print(
                    f"{i}: {fields['IDKSIP']}, drv_b: {fields['driver behavior']}, ped_b: {fields['pedestrian behavior']}, notes: {fields['other']}"
                )


class AccidentView(ListView):
    data_names = {
        "district": District,
        "driver_behavior": DriverBehavior,
        "lighting": Lighting,
        "notes": Notes,
        "pedestrian_behavior": PedestrianBehavior,
        "place_of_the_event": PlaceOfTheEvent,
        "road": Road,
        "road_category": RoadCategory,
        "road_geometry": RoadGeometry,
        "town": Town,
        "type_of_accident": TypeOfAccident,
        "type_of_injury": TypeOfInjury,
        "voivodeship": Voivodeship,
        "weather_conditions": WeatherConditions,
        "is_built_up_area": Accident.is_built_up_area,
        "data_time": Accident.data_time,
        "num_of_accidents": Accident.num_of_accidents,
        "num_of_fatalities": Accident.num_of_fatalities,
        "num_of_injured": Accident.num_of_injured,
        "is_offender_intoxicated": Accident.is_offender_intoxicated,
    }

    def get_request_data(self, request):
        if request.method == "POST":
            district = request.POST.get("district")
            driver_behavior = request.POST.get("driver_behavior")
            lighting = request.POST.get("lighting")
            notes = request.POST.get("notes")
            pedestrian_behavior = request.POST.get("pedestrian_behavior")
            place_of_the_event = request.POST.get("place_of_the_event")
            road = request.POST.get("road")
            road_category = request.POST.get("road_category")
            road_geometry = request.POST.get("road_geometry")
            town = request.POST.get("town")
            type_of_accident = request.POST.get("type_of_accident")
            type_of_injury = request.POST.get("type_of_injury")
            voivodeship = request.POST.get("voivodeship")
            weather_conditions = request.POST.get("weather_conditions")
            is_built_up_area = request.POST.get("is_built_up_area")
            data_time = request.POST.get("data_time")
            num_of_accidents = request.POST.get("num_of_accidents")
            num_of_fatalities = request.POST.get("num_of_fatalities")
            num_of_injured = request.POST.get("num_of_injured")
            is_offender_intoxicated = request.POST.get("is_offender_intoxicated")
            return [
                district,
                driver_behavior,
                lighting,
                notes,
                pedestrian_behavior,
                place_of_the_event,
                road,
                road_category,
                road_geometry,
                town,
                type_of_accident,
                type_of_injury,
                voivodeship,
                weather_conditions,
                is_built_up_area,
                data_time,
                num_of_accidents,
                num_of_fatalities,
                num_of_injured,
                is_offender_intoxicated,
            ]
        else:
            return []

    def collect_data_from_db(self, request):
        post_data = self.get_request_data(request)
        post_collected_data = []
        for data in post_data:
            if data:
                data = self.data_names[data].objects.get(data)
            else:
                data = self.data_names[data].objects.all()
            post_collected_data.append(data)
        return post_collected_data

    def create_view(self, request):
        data = self.collect_data_from_db(request)
        result_filter = {}
        for current_filter in data:
            result_filter[current_filter] = current_filter
        return render(
            request,
            'fronted/filter_test.html',
            {
                "district": result_filter["district"],
                "driver_behavior": result_filter["driver_behavior"],
                "lighting": result_filter["lighting"],
                "notes": result_filter["notes"],
                "pedestrian_behavior": result_filter["pedestrian_behavior"],
                "place_of_the_event": result_filter["place_of_the_event"],
                "road": result_filter["road"],
                "road_category": result_filter["road_category"],
                "road_geometry": result_filter["road_geometry"],
                "town": result_filter["town"],
                "type_of_accident": result_filter["type_of_accident"],
                "type_of_injury": result_filter["type_of_injury"],
                "voivodeship": result_filter["voivodeship"],
                "weather_conditions": result_filter["weather_conditions"],
                "is_built_up_area": result_filter["is_built_up_area"],
                "data_time": result_filter["data_time"],
                "num_of_accidents": result_filter["num_of_accidents"],
                "num_of_fatalities": result_filter["num_of_fatalities"],
                "num_of_injured": result_filter["num_of_injured"],
                "is_offender_intoxicated": result_filter["is_offender_intoxicated"],
            }
        )
