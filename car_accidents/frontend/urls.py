from django.urls import path

from . import views


app_name = 'frontend'

urlpatterns = [
    path('', views.filters_form, name='filters_form'),
]
