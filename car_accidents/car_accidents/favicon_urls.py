from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic.base import RedirectView


favicon_patterns = [
    path(
        'apple-icon-57x57.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/apple-icon-57x57.png")),
    ),
    path(
        'apple-icon-60x60.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/apple-icon-60x60.png")),
    ),
    path(
        'apple-icon-72x72.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/apple-icon-72x72.png")),
    ),
    path(
        'apple-icon-76x76.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/apple-icon-76x76.png")),
    ),
    path(
        'apple-icon-114x114.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/apple-icon-114x114.png")),
    ),
    path(
        'apple-icon-120x120.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/apple-icon-120x120.png")),
    ),
    path(
        'apple-icon-144x144.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/apple-icon-144x144.png")),
    ),
    path(
        'apple-icon-152x152.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/apple-icon-152x152.png")),
    ),
    path(
        'apple-icon-180x180.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/apple-icon-180x180.png")),
    ),
    path(
        'android-icon-192x192.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/android-icon-192x192.png")),
    ),
    path(
        'favicon-32x32.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/favicon-32x32.png")),
    ),
    path(
        'favicon-96x96.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/favicon-96x96.png")),
    ),
    path(
        'favicon-16x16.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/favicon-16x16.png")),
    ),
    path('manifest.json', RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/manifest.json"))),
    path(
        'ms-icon-144x144.png',
        RedirectView.as_view(url=staticfiles_storage.url("frontend/images/favicons/ms-icon-144x144.png")),
    ),
]
