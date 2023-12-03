from django.urls import path
from .views import KPI1View, KPI2View

urlpatterns = [
    path('api/kpi1/', KPI1View.as_view(), name='kpi1_api'),
    path('api/kpi2/', KPI2View.as_view(), name='kpi2_api'),
]