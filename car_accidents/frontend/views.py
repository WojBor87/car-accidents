from django.shortcuts import render
from django.views.generic import View, ListView
from django.db import connection
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path
from .models import (
    RoadCategory,
    Road,
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


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{120*" "}\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print(flush=True)


# Create your views here.
def filters_form(request):
    db_name = connection.settings_dict['NAME']
    return render(request, 'frontend/filters_form.html', {'db_name': db_name})


class ImportCsvView(View):
    def get(self, request, file_name):
        pd.set_option('display.max_columns', None)
        self.df = pd.read_csv('frontend/static/frontend/csv' / Path(file_name))
        self.updated_and_created_rows = [0, 0]
        self.df = self.df[self.df['IDKSIP'].str.startswith('EWK-')]
        self.process_behavior() if 'driver behavior' in self.df else self.process_all()
        self.insert_or_replace_behavior() if 'driver behavior' in self.df else self.insert_or_replace_all()

        return render(request, 'frontend/import_csv.html', {'updated_and_created_rows': self.updated_and_created_rows})

    def process_all(self):
        # drop shifted data TODO: clear it so those rows can be used
        self.df['Longitude'] = self.df['Longitude'].astype(str)
        self.df.query(
            'not(district == ["T", "N"] or district_commune.str.contains("POWIAT") or is_offender_intoxicated != ["T", "N"] or Longitude.str.contains("1\.1900") or Longitude.str.contains("#"))',
            inplace=True,
        )
        self.df['hour'].apply(int)
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
        printProgressBar(0, len(self.df), prefix=f'{self.df.count()} items, Progress: ', suffix='processed', length=50)
        for i, *fields in self.df.itertuples():
            fields_dict = dict(zip(self.df.columns, fields))
            printProgressBar(
                i + 1, len(self.df), prefix=f'{len(self.df)} items, Progress: ', suffix='processed', length=50
            )
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

            datetime_of_accident = datetime.strptime(f"{fields_dict['date']} {fields_dict['hour']}", r'%Y-%m-%d %H')
            datetime_of_accident = timezone.make_aware(
                datetime_of_accident, timezone.get_current_timezone(), is_dst=True
            )

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


class AccidentView(ListView):

    model = Accident
    template_name = "frontend/accident_view.html"
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    #
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
    #     if request.method == "POST":
    #         district = request.POST.get("district")
    #         driver_behavior = request.POST.get("driver_behavior")
    #         lighting = request.POST.get("lighting")
    #         notes = request.POST.get("notes")
    #         pedestrian_behavior = request.POST.get("pedestrian_behavior")
    #         place_of_the_event = request.POST.get("place_of_the_event")
    #         road = request.POST.get("road")
    #         road_category = request.POST.get("road_category")
    #         road_geometry = request.POST.get("road_geometry")
    #         town = request.POST.get("town")
    #         type_of_accident = request.POST.get("type_of_accident")
    #         type_of_injury = request.POST.get("type_of_injury")
    #         voivodeship = request.POST.get("voivodeship")
    #         weather_conditions = request.POST.get("weather_conditions")
    #         is_built_up_area = request.POST.get("is_built_up_area")
    #         data_time = request.POST.get("data_time")
    #         num_of_accidents = request.POST.get("num_of_accidents")
    #         num_of_fatalities = request.POST.get("num_of_fatalities")
    #         num_of_injured = request.POST.get("num_of_injured")
    #         is_offender_intoxicated = request.POST.get("is_offender_intoxicated")
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
