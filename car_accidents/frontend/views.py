from django.shortcuts import render
from django.views.generic import View
from django.db import connection
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from datetime import datetime
import pytz
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
        self.updated_and_created_rows = [0, 0]
        self.process_behavior() if 'driver behavior' in self.df else self.process_all()
        self.insert_or_replace_behavior() if 'driver behavior' in self.df else self.insert_or_replace_all()

        return render(request, 'frontend/import_csv.html', {'updated_and_created_rows': self.updated_and_created_rows})

    def process_all(self):
        # drop shifted data TODO: clear it so those rows can be used
        self.df['Longitude'] = self.df['Longitude'].astype(str)
        self.df.query(
            'not(district == ["T", "N"] or district_commune.str.contains("POWIAT") or is_offender_intoxicated != ["T", "N"] or Longitude.str.contains("1\.1900"))',
            inplace=True,
        )
        self.df['road_category'].replace('Nieokreślone (puste pole)', np.nan, inplace=True)
        self.df['road_number'].replace('0', np.nan, inplace=True)
        self.df['district'] = self.df['district'].str.replace('POWIAT ', '')
        self.df[['town', 'is_city']] = self.df['district_commune'].str.split(' - ', 1, expand=True)
        booleanDictionary = {'OBSZAR MIEJSKI': True, 'OBSZAR WIEJSKI': False}
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
            fields_dict = dict(zip(self.df.columns, fields))
            RoadCategory_obj, if_created = RoadCategory.objects.update_or_create(
                name=fields_dict['road_category'],
                defaults={
                    'name': fields_dict['road_category'],
                },
            )
            self.updated_and_created_rows[if_created] += 1

            Road_obj, if_created = Road.objects.update_or_create(
                name=fields_dict['road_number'],
                defaults={
                    'name': fields_dict['road_number'],
                    'road_category_id': RoadCategory_obj,
                },
            )
            self.updated_and_created_rows[if_created] += 1

            District_obj, if_created = District.objects.update_or_create(
                name=fields_dict['district'],
                defaults={
                    'name': fields_dict['district'],
                    'voivodeship_id': None,
                },
            )
            self.updated_and_created_rows[if_created] += 1

            Town_obj, if_created = Town.objects.update_or_create(
                name=fields_dict['town'],
                defaults={
                    'name': fields_dict['town'],
                    'district_id': District_obj,
                    'is_city': fields_dict['is_city'],
                },
            )
            self.updated_and_created_rows[if_created] += 1

            RoadGeometry_obj, if_created = RoadGeometry.objects.update_or_create(
                name=fields_dict['road_geometry'],
                defaults={
                    'name': fields_dict['road_geometry'],
                },
            )
            self.updated_and_created_rows[if_created] += 1

            PlaceOfTheEvent_obj, if_created = PlaceOfTheEvent.objects.update_or_create(
                name=fields_dict['char_place_of_the_event'],
                defaults={
                    'name': fields_dict['char_place_of_the_event'],
                },
            )
            self.updated_and_created_rows[if_created] += 1

            TypeOfInjury_obj, if_created = TypeOfInjury.objects.update_or_create(
                name=fields_dict['type_of_injury'],
                defaults={
                    'name': fields_dict['type_of_injury'],
                },
            )
            self.updated_and_created_rows[if_created] += 1

            TypeOfAccident_obj, if_created = TypeOfAccident.objects.update_or_create(
                name=fields_dict['type_of_accident'],
                defaults={
                    'name': fields_dict['type_of_accident'],
                },
            )
            self.updated_and_created_rows[if_created] += 1

            Lighting_obj, if_created = Lighting.objects.update_or_create(
                name=fields_dict['lighting'],
                defaults={
                    'name': fields_dict['lighting'],
                },
            )
            self.updated_and_created_rows[if_created] += 1

            WeatherConditions_obj, if_created = WeatherConditions.objects.update_or_create(
                name=fields_dict['weather_conditions'],
                defaults={
                    'name': fields_dict['weather_conditions'],
                },
            )
            self.updated_and_created_rows[if_created] += 1

            datetime_of_accident = datetime.strptime(f"{fields_dict['date']} {fields_dict['hour']:02}", r'%Y-%m-%d %H')
            datetime_of_accident = timezone.make_aware(datetime_of_accident, timezone.get_current_timezone())

            Accident_obj, if_created = Accident.objects.update_or_create(
                idksip=fields_dict['IDKSIP'],
                defaults={
                    'idksip': fields_dict['IDKSIP'],
                    'data_time': datetime_of_accident,
                    'town_name': Town_obj,
                    'road': Road_obj,
                    'is_built_up_area': fields_dict['area'],
                    'longitude': fields_dict['Longitude'],
                    'latitude': fields_dict['Latitude'],
                    'road_geometry': RoadGeometry_obj,
                    'place_of_the_event': PlaceOfTheEvent_obj,
                    'weather_conditions': WeatherConditions_obj,
                    'lighting': Lighting_obj,
                    'type_of_accident': TypeOfAccident_obj,
                    'num_of_accidents': fields_dict['num_of_accidents'],
                    'num_of_fatalities': fields_dict['num_of_fatalities'],
                    'num_of_injured': fields_dict['num_of_injured'],
                    'type_of_injury': TypeOfInjury_obj,
                    'is_offender_intoxicated': fields_dict['is_offender_intoxicated'],
                },
            )
            self.updated_and_created_rows[if_created] += 1

    def insert_or_replace_behavior(self):
        for i, *fields in self.df.itertuples():
            fields_dict = dict(zip(self.df.columns, fields))
            if Accident.objects.filter(idksip=fields_dict['IDKSIP']):
                PedestrianBehavior_obj, if_created = PedestrianBehavior.objects.update_or_create(
                    name=fields_dict['pedestrian behavior'],
                    defaults={
                        'name': fields_dict['pedestrian behavior'],
                    },
                )
                self.updated_and_created_rows[if_created] += 1

                DriverBehavior_obj, if_created = DriverBehavior.objects.update_or_create(
                    name=fields_dict['driver behavior'],
                    defaults={
                        'name': fields_dict['driver behavior'],
                    },
                )
                self.updated_and_created_rows[if_created] += 1

                Notes_obj, if_created = Notes.objects.update_or_create(
                    name=fields_dict['other'],
                    defaults={
                        'name': fields_dict['other'],
                    },
                )
                self.updated_and_created_rows[if_created] += 1
                accident_field = Accident.objects.get(idksip=fields_dict['IDKSIP'])
                accident_field.driver_behavior = DriverBehavior_obj
                accident_field.pedestrian_behavior = PedestrianBehavior_obj
                accident_field.notes = Notes_obj
                accident_field.save()
