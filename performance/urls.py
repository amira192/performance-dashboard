from django.urls import path
from .views import (
    AdminDashboardView, ManagerDashboardView, StudentDashboardView,
    FeedbackListView, FeedbackCreateView, TaskListView
)
from . import views

urlpatterns = [
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('dashboard/manager/', ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('dashboard/student/', StudentDashboardView.as_view(), name='student_dashboard'),

    path('feedbacks/', FeedbackListView.as_view(), name='feedback_list'),
    path('feedbacks/add/', FeedbackCreateView.as_view(), name='feedback_add'),

    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
    path('tasks/export/csv/', views.export_tasks_csv, name='export_tasks_csv'),
]
