from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from datetime import datetime
from .consistency_check import check_consistency

class ConsistencyCheckView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        timestamps = request.data.get("timestamps", [])
        if not isinstance(timestamps, list):
            return Response(
                {"error": "timestamps must be a list of date strings."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            parsed_dates = [datetime.strptime(ts, "%Y-%m-%d") for ts in timestamps]
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        result = check_consistency(parsed_dates)
        return Response(result)
            
        