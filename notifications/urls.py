from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications_list, name='notifications_list'),  # main notifications page / dropdown
    path('count/', views.notifications_count, name='notifications_count'),  # AJAX: unread count
    path('mark-read/', views.mark_notification_read, name='mark_notification_read'),  # AJAX: mark read
]
