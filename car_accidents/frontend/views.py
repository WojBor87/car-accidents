from django.shortcuts import render, HttpResponse
from django.views.generic import View
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

