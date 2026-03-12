from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import PeriodEntry, CycleStart
from rest_framework.generics import ListCreateAPIView
from .serializers import (
    PeriodEntrySerializer, 
    CycleStartSerializer, 
    CustomUserSerializer,
    CustomUserRegistrationSerializer
)

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]  
    authentication_classes = []      

    def post(self, request):
        serializer = CustomUserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "user": CustomUserSerializer(user).data,
                "token": token.key},
                status=status.HTTP_201_CREATED          
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        })

        
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "typical_cycle_length": user.typical_cycle_length
        })
        
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

class CycleStartListAPIView(ListCreateAPIView):
    queryset = CycleStart.objects.all()
    serializer_class = CycleStartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CycleStart.objects.filter(user=self.request.user).order_by('-id')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    
    
