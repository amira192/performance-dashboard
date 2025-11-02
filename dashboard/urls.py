from django.urls import path
from .views import (
    AdminDashboardView, ManagerDashboardView, StudentDashboardView,
    student_chart_data, admin_chart_data, manager_chart_data
)
from . import views

urlpatterns = [
    path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('manager/', ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('student/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('student/chart-data/', student_chart_data, name='student_chart_data'),
    path('admin/chart-data/', admin_chart_data, name='admin_chart_data'),
    path('manager/chart-data/', manager_chart_data, name='manager_chart_data'),
    path('export-tasks-csv/', views.export_tasks_csv, name='export_tasks_csv'),
]
