from django.contrib import admin
from django.urls import path, include
from .favicon_urls import favicon_patterns
from django.contrib.auth import views as auth_views


urlpatterns = (
    [path('admin/', admin.site.urls)]
    + favicon_patterns
    + [
        path('', include('frontend.urls')),
        path('login/', auth_views.LoginView.as_view(), name="login"),
        path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    ]
)
