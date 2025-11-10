from django.urls import path
from .views import DashboardView, dashboard_chart_data
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('chart-data/', views.dashboard_chart_data, name='dashboard_chart_data'),
]
