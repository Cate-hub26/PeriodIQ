from django.contrib import admin
from .models import CustomUser, PeriodEntry, CycleStart

admin.site.register(CustomUser)
admin.site.register(PeriodEntry)
admin.site.register(CycleStart)