from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from .models import KPI1, KPI2

class KPI1View(View):
    def get(self, request, *args, **kwargs):
        start_time = int(request.GET.get('start_time', 0))
        end_time = int(request.GET.get('end_time', 9999999999999))
        interval_period = request.GET.get('interval_period', '5-minute')

        kpi1_data = KPI1.objects.filter(
            interval_start_timestamp__gte=start_time,
            interval_end_timestamp__lte=end_time,
            interval_period=interval_period
        ).values()

        return JsonResponse({'kpi1_data': list(kpi1_data)})

class KPI2View(View):
    def get(self, request, *args, **kwargs):
        start_time = int(request.GET.get('start_time', 0))
        end_time = int(request.GET.get('end_time', 9999999999999))
        interval_period = request.GET.get('interval_period', '5-minute')

        kpi2_data = KPI2.objects.filter(
            interval_start_timestamp__gte=start_time,
            interval_end_timestamp__lte=end_time,
            interval_period=interval_period
        ).values()

        return JsonResponse({'kpi2_data': list(kpi2_data)})
    
    