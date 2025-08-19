from django.urls import path
from .cycle_summary import CycleSummaryView
from .consistency_check_views import ConsistencyCheckView
from .predictions_views import PredictionView
from .views import (
    PeriodEntriesListCreateAPIView,
    PeriodEntriesRetrieveUpdateDestroyAPIView,
    CycleStartListAPIView, UserProfileView,
    CustomLoginView, RegisterView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='custom-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
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
    path('cycle-summary/', CycleSummaryView.as_view(), name='cycle-summary'),
    path('consistency-check/', ConsistencyCheckView.as_view(), name='consistency-check'),
    path('prediction/', PredictionView.as_view(), name='prediction')   
]