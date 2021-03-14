from django.urls import path, include

from . import views


app_name = 'frontend'

urlpatterns = [
    path('', views.filters_form, name='filters_form'),
    path('helper/', include('frontend.helper_urls')),
    path('import_csv/<file_name>', views.ImportCsvView.as_view(), name='import_csv'),
    path('accident_view/', views.AccidentView.as_view(), name='accident_view'),
    path('accident_filter_view/', views.filter_search, name='filter'),
    path('fatal-accident-map-view/', views.FatalAccidentMapView, name='fatal-map'),
]
