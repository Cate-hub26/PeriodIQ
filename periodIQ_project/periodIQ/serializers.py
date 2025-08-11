from rest_framework import serializers
from .models import CustomUser, PeriodEntry, CycleStart

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'typical_cycle_length']
        
class PeriodEntrySerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = PeriodEntry
        fields = ['user', 'start_date']
        
class CycleStartSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = CycleStart
        fields = [
                  'user', 
                  'average_cycle', 
                  'min_cycle', 
                  'max_cycle', 
                  'irregular_flag'
        ]