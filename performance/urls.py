from django.urls import path
from .views import (
    DashboardView, FeedbackListView, FeedbackCreateView, TaskListView,
    AddStudentView, task_create, task_update, task_delete,
    export_tasks_csv, AddCourseView, LeaveCreateView, LeaveListView
)
from . import views


urlpatterns = [

    # Dashboard (Unified)
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Feedback
    path('feedbacks/', FeedbackListView.as_view(), name='feedback_list'),
    path('feedbacks/add/', FeedbackCreateView.as_view(), name='add_feedback'),

    # Tasks
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/create/', task_create, name='task_create'),
    path('tasks/<int:pk>/edit/', task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', task_delete, name='task_delete'),
    path('tasks/export/csv/', export_tasks_csv, name='export_tasks_csv'),

    # Students
    path('add-student/', AddStudentView.as_view(), name='add_student'),
    path('add-course/', AddCourseView.as_view(), name='add_course'),

    # Leaves
    path('leaves/', LeaveListView.as_view(), name='leave_list'),
    path('leaves/add/', LeaveCreateView.as_view(), name='add_leave'),

    # Course
    path('add-course/', AddCourseView.as_view(), name='add_course'),

]
