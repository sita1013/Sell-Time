from django.contrib import admin
from .models import TimePackage

@admin.register(TimePackage)
class TimePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes', 'price', 'use_type')
    search_fields = ('name',)
    list_filter = ('use_type',)
