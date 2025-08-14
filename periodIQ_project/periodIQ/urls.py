from django.urls import path
from .views import (
    PeriodEntriesListCreateAPIView,
    PeriodEntriesRetrieveUpdateDestroyAPIView,
    CycleStartListAPIView
)

urlpatterns = [
    path(
        'period/', 
         PeriodEntriesListCreateAPIView.as_view(), 
         name='periodentry-list-create'
    ),
    path(
        'period/<int:pk>/',
         PeriodEntriesRetrieveUpdateDestroyAPIView.as_view(), 
         name='periodentry-retrieve-update-destroy'
    ),
    path(
        'cycle-start/', 
         CycleStartListAPIView.as_view(), 
         name='cyclestart-list-create'
    ),
]