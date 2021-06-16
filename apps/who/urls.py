from django.urls import path

from .views import IndexView, ResultsView, SubmitView, verify_query

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('results/', verify_query, name='verify'),
    path('results/<str:login>/', ResultsView.as_view(), name='results'),
]