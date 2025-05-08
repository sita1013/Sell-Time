from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from django.utils.timezone import now, timedelta
from .models import TimePackage, Purchase


@admin.register(TimePackage)
class TimePackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration_minutes', 'price', 'use_type')
    search_fields = ('name',)
    list_filter = ('use_type',)

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    change_list_template = "admin/purchase_data.html"
    def changelist_view(self, request, extra_context=None):
        today = now().date()
        last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
        labels = [day.strftime('%Y-%m-%d') for day in last_7_days]
        counts = [
            Purchase.objects.filter(timestamp__date=day).count()
            for day in last_7_days
        ]
        extra_context = extra_context or {}
        extra_context["labels"] = labels
        extra_context["counts"] = counts
        return super().changelist_view(request, extra_context=extra_context)