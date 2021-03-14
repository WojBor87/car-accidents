from django.urls import path, include

from . import views


app_name = 'frontend'

urlpatterns = [
    path('', views.filter_search, name='filter'),
    path('helper/', include('frontend.helper_urls')),
    path('import_csv/<file_name>', views.ImportCsvView.as_view(), name='import_csv'),
]
