import folium as folium
from django.shortcuts import render
from django.views.generic import View, ListView, TemplateView
from django.db import connection
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .filters import AccidentFilter
import pandas as pd
import numpy as np
from pathlib import Path
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        self.df = self.df[self.df['IDKSIP'].str.startswith('EWK-')]
        self.process_behavior() if 'driver behavior' in self.df else self.process_all()
        self.insert_or_replace_behavior() if 'driver behavior' in self.df else self.insert_or_replace_all()

        return render(request, 'frontend/import_csv.html', {'updated_and_created_rows': self.updated_and_created_rows})

    def printProgressBar(
            self, iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"
    ):
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
        print(f'\r{120 * " "}\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
        # Print New Line on Complete
        if iteration == total:
            print(flush=True)

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
        self.printProgressBar(
            0, len(self.df), prefix=f'{self.df.count()} items, Progress: ', suffix='processed', length=50
        )
        for i, *fields in self.df.itertuples():
            fields_dict = dict(zip(self.df.columns, fields))
            self.printProgressBar(
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
        context = super(AccidentView, self).get_context_data(**kwargs)
        return context


def filter_search(request):
    accident_list = Accident.objects.all().order_by('-data_time')
    accident_filter = AccidentFilter(request.GET, queryset=accident_list)
    paginator = Paginator(accident_filter.qs, 15)
    page = request.GET.get('page')
    try:
        dataqs = paginator.page(page)
    except PageNotAnInteger:
        dataqs = paginator.page(1)
    except EmptyPage:
        dataqs = paginator.page(paginator.num_pages)

    return render(
        request,
        'frontend/accident_filter_view.html',
        {
            'accident_list': accident_list,
            'accident_filter': accident_filter,
            'dataqs': dataqs,
        },
    )


data = pd.read_csv("/home/michalm/PycharmProjects/car-accidents/car_accidents/frontend/static/frontend/csv/all.csv")


class FatalAccidentMapView(TemplateView):
    template_name = "frontend/map.html"

    def get_context_data(self, **kwargs):
        figure = folium.Figure()
        m = folium.Map(location=[52.272185, 21.007728], zoom_start=12)
        m.add_ro(figure)

        for lat, long, labels in zip(data.Latitude, data.Longitude, data.num_of_fatalities.astype(str)):
            if labels != '0':
                folium.CircleMarker(
                    (lat, long),
                    radius=3,
                    color='red',
                    fill=True,
                    popup=labels,
                    fill_color='darkred',
                    fill_opacity=0.6).add_to(m)
        m.add_to(figure)
        figure.render()
        return {"map": figure}

