from django.contrib import admin
from .models import Accident

@admin.register(Accident)
class AccidentAdmin(admin.ModelAdmin):
    list_display = ["idksip", "data_time", "town_name", "road"]
    list_filter = ["idksip", "data_time", "town_name", "road"]
    search_fields = ["idksip", "road"]