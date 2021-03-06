from django.contrib import admin
from django.urls import path, include
from .favicon_urls import favicon_patterns

urlpatterns = (
    [path('admin/', admin.site.urls)]
    + favicon_patterns
    + [
        path('', include('frontend.urls')),
    ]
)
