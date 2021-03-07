from django.shortcuts import render, HttpResponse
from django.db import connection
import pandas as pd
from pathlib import Path


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
