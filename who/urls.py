from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

from .views import IndexView, ResultsView, verify_query

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('who/', verify_query, name='verify'),
    path('who/results/<str:login>/', ResultsView.as_view(), name='results'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
]

urlpatterns += staticfiles_urlpatterns()