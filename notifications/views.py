from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.http import JsonResponse
from django.views import View
from accounts.models import UserProfile


class AdminDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.userprofile.role != 'admin':
            return HttpResponseForbidden("You are not authorized to view this page.")
        return render(request, 'dashboard/admin_dashboard.html')


class ManagerDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.userprofile.role != 'manager':
            return HttpResponseForbidden("You are not authorized to view this page.")
        students = UserProfile.objects.filter(role='student')
        return render(request, 'dashboard/manager_dashboard.html', {'students': students})


class StudentDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.userprofile.role != 'student':
            return HttpResponseForbidden("You are not authorized to view this page.")
        return render(request, 'dashboard/student_dashboard.html')

@login_required
def notifications_list(request):
    notifications = request.user.notifications.all().order_by('-created_at')
    return render(request, 'notifications/notifications.html', {'notifications': notifications})

@login_required
def notifications_count(request):
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({'unread_count': count})

@login_required
@require_POST
def mark_notification_read(request):
    notif_id = request.POST.get('id')
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return JsonResponse({'success': True})