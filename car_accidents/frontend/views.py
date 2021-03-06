from django.shortcuts import render
from django.db import connection


# Create your views here.
def filters_form(request):
    db_name = connection.settings_dict['NAME']
    print('db_name: ', db_name)
    return render(request, 'frontend/filters_form.html', {'db_name': db_name})
