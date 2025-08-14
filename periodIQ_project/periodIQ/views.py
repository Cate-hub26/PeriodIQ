from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PeriodEntry, CycleStart
from .serializers import PeriodEntrySerializer, CycleStartSerializer

class PeriodEntriesListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PeriodEntrySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PeriodEntry.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
class PeriodEntriesRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PeriodEntrySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PeriodEntry.objects.filter(user=self.request.user)

class CycleStartListAPIView(generics.ListAPIView):
    serializer_class = CycleStartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CycleStart.objects.filter(user=self.request.user)
    
    
    
