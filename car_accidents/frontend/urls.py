from django.urls import path, include

from . import views


app_name = 'frontend'

urlpatterns = [
<<<<<<< Updated upstream
    path('', views.home, name='home'),
=======
    path('', views.filters_form, name='filters_form'),
    path('helper/', include('frontend.helper_urls')),
    path('import_csv/<file_name>', views.import_csv, name='import_csv'),
>>>>>>> Stashed changes
]
