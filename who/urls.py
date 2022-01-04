from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import IndexView, ResultsView, verify_query

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('who/', verify_query, name='verify'),
    path('who/results/<str:login>/', ResultsView.as_view(), name='results'),
]

urlpatterns += staticfiles_urlpatterns()