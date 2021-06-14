from django.urls import path

from .views import IndexView, ResultsView, SubmitView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('results/', SubmitView.as_view(), name='submit-view'),
    path('results/<str:pk>/', ResultsView.as_view(), name='results'),
]