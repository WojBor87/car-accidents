from django.urls import path, include

from . import views


app_name = 'frontend'

urlpatterns = [
    path('', views.filter_search, name='filter'),
    path('helper/', include('frontend.helper_urls')),
    path('import_csv/<file_name>', views.ImportCsvView.as_view(), name='import_csv'),
    path('fatal-accident-map/', views.show_map, name='fatal-map'),
    path('all-accident-map/', views.show_fatalities_map, name='all-accident-map'),
]
