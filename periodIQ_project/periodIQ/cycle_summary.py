from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import PeriodEntry
from .utils.calculations import (
    calculate_period_duration, 
    calculate_cycle_lengths, 
    average_cycle_length
)

class CycleSummaryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        entries = PeriodEntry.objects.filter(user=user).order_by('start_date')
        
        if not entries.exists():
            return Response({
                "message": "No period entries found.",
                "average_cycle_length": 0.0,
                "average_period_duration": 0
            })
            
        entry_data = []
        period_durations = []
        
        for entry in entries:
            if entry.end_date:
                duration = calculate_period_duration(
                    entry.start_date.strftime('%Y-%m-%d'),
                    entry.end_date.strftime('%Y-%m-%d')
                )
                period_durations.append(duration)
                
            entry_data.append({
                'start_date': entry.start_date.strftime('%Y-%m-%d')
            })
            
        cycle_lengths = calculate_cycle_lengths(entry_data)
        avg_cycle = average_cycle_length(cycle_lengths)
        avg_period_duration = round(sum(period_durations) / len(period_durations), 2) if period_durations else 0 
        
        return Response({
            "average_cycle_length": avg_cycle,
            "average_period_duration": avg_period_duration,
            "entry_count": entries.count()
        })

        

        
    
