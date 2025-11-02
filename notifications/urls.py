from django.urls import path
from .views import notifications_list, notifications_count, mark_notification_read

urlpatterns = [
    path('', notifications_list, name='notifications_list'),
    path('count/', notifications_count, name='notifications_count'),
    path('mark-read/', mark_notification_read, name='mark_notification_read'),

]
