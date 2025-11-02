# dashboard/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views import View

from accounts.models import UserProfile
from performance.models import Task, Submission
from notifications.models import Notification
from django.http import HttpResponse
import csv

# ==========================
# Dashboard Views
# ==========================
class AdminDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.userprofile.role != 'admin':
            return HttpResponseForbidden("You are not authorized to view this page.")

        total_students = UserProfile.objects.filter(role='student').count()
        total_managers = UserProfile.objects.filter(role='manager').count()
        pending_tasks = Task.objects.filter(status='pending').count()

        context = {
            'total_students': total_students,
            'total_managers': total_managers,
            'pending_tasks': pending_tasks,
        }
        return render(request, 'dashboard/admin_dashboard.html', context)


class ManagerDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.userprofile.role != 'manager':
            return HttpResponseForbidden("You are not authorized to view this page.")

        students = UserProfile.objects.filter(role='student')
        pending_tasks = Task.objects.filter(status='pending').count()
        context = {
            'students': students,
            'pending_tasks': pending_tasks,
        }
        return render(request, 'dashboard/manager_dashboard.html', context)


class StudentDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.userprofile.role != 'student':
            return HttpResponseForbidden("You are not authorized to view this page.")

        student = request.user
        completed = Submission.objects.filter(student=student, status='completed').count()
        pending = Submission.objects.filter(student=student, status='pending').count()

        context = {
            'completed': completed,
            'pending': pending,
        }
        return render(request, 'dashboard/student_dashboard.html', context)


# ==========================
# AJAX Chart Data Views
# ==========================
@login_required
def admin_chart_data(request):
    if request.user.userprofile.role != 'admin':
        return HttpResponseForbidden()

    data = {
        'total_students': UserProfile.objects.filter(role='student').count(),
        'total_managers': UserProfile.objects.filter(role='manager').count(),
        'pending_tasks': Task.objects.filter(status='pending').count()
    }
    return JsonResponse(data)


@login_required
def manager_chart_data(request):
    if request.user.userprofile.role != 'manager':
        return HttpResponseForbidden()

    students = UserProfile.objects.filter(role='student')
    labels = []
    completed = []
    pending = []

    for student in students:
        labels.append(student.user.username)
        completed.append(Submission.objects.filter(student=student.user, status='completed').count())
        pending.append(Submission.objects.filter(student=student.user, status='pending').count())

    data = {'labels': labels, 'completed': completed, 'pending': pending}
    return JsonResponse(data)


@login_required
def student_chart_data(request):
    if request.user.userprofile.role != 'student':
        return HttpResponseForbidden()

    student = request.user
    data = {
        'completed': Submission.objects.filter(student=student, status='completed').count(),
        'pending': Submission.objects.filter(student=student, status='pending').count()
    }
    return JsonResponse(data)


# ==========================
# Notifications Views
# ==========================
@login_required
def notifications_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/notifications.html', {'notifications': notifications})


@login_required
def notifications_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})


@login_required
@require_POST
def mark_notification_read(request):
    notif_id = request.POST.get('id')
    notif = get_object_or_404(Notification, id=notif_id, user=request.user)
    notif.is_read = True
    notif.save()
    return JsonResponse({'success': True})

def export_tasks_csv(request):
    # your CSV export logic
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'
    writer = csv.writer(response)
    writer.writerow(['Task', 'Status'])
    # write tasks
    return response