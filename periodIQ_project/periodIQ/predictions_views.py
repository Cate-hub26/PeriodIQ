from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .utils.predictions import predict_next_period

class PredictionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        cycle_data = request.data.get("cycle_data", [])
        
        result = predict_next_period(cycle_data)
        
        if "error" in result:
            return Response(result, status=400)
        return Response(result)
        