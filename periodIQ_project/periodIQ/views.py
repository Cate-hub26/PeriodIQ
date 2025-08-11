from django.shortcuts import render
from rest_framework import generics
from .models import PeriodEntry, CycleStart
from .serializers import CustomUserSerializer, PeriodEntrySerializer, CycleStartSerializer

class PeriodEntriesListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PeriodEntrySerializer
    
    def get_queryset(self):
        return PeriodEntry.objects.filter(user=self.request.user)
        
class PeriodEntriesListRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PeriodEntrySerializer
    
    def get_queryset(self):
        return PeriodEntry.objects.filter(user=self.request.user)

class CycleStartListAPIView(generics.ListAPIView):
    serializer_class = CycleStartSerializer
    
    def get_queryset(self):
        return CycleStart.objects.filter(user=self.request.user)

    
    
