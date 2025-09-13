from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    typical_cycle_length = models.IntegerField(default=28)
    
    def __str__(self):
        return self.username
        
    
class PeriodEntry(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='period_entries'
    )
    start_date = models.DateField()
    
    end_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.start_date} to {self.end_date}"
    
class CycleStart(models.Model):
    user = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='cycle_start'
    )
    average_cycle = models.IntegerField()
    min_cycle = models.IntegerField()
    max_cycle = models.IntegerField()
    irregular_flag = models.BooleanField()
    
    def __str__(self):
        return f"{self.user.username} - Cycle Avg: {self.average_cycle}"
    



