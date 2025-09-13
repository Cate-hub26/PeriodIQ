from rest_framework import serializers
from .models import CustomUser, PeriodEntry, CycleStart
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'typical_cycle_length']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            typical_cycle_length=validated_data.get('typical_cycle_length', 28)
        )
        return user
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'typical_cycle_length']
        read_only_fields = ['id', 'email', 'username', 'typical_cycle_length']
             
class PeriodEntrySerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    class Meta:
        model = PeriodEntry
        fields = ['user', 'start_date', 'end_date']
        
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
        
class ConsistencyResultSerializer(serializers.Serializer):
    status = serializers.CharField()
    average_gap = serializers.FloatField(allow_null=True)
    min_gap = serializers.FloatField(allow_null=True)
    max_gap = serializers.FloatField(allow_null=True)
    std_dev = serializers.FloatField(allow_null=True)
    is_consistent = serializers.BooleanField(allow_null=True)