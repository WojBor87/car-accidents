from django.urls import path, include

from . import views


app_name = 'frontend'

urlpatterns = [
    path('', views.home, name='home'),
    path('helper/', include('frontend.helper_urls')),
    path('import_csv/<file_name>', views.ImportCsvView.as_view(), name='import_csv'),
    path('accident_filter_view/', views.filter_search, name='filter')
]
