from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponseForbidden, JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from performance.models import Task, Submission
from accounts.models import UserProfile
from performance.models import Course

# ==========================
# Unified Dashboard View (CBV)
# ==========================
class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        role = user.userprofile.role

        total_students = UserProfile.objects.filter(role='student').count()
        total_teachers = UserProfile.objects.filter(role='teacher').count()
        total_courses = Course.objects.count()
        total_tasks = Task.objects.count()
        completed_tasks = Submission.objects.filter(status='completed').count()
        pending_tasks = Submission.objects.filter(status='pending').count()

        context = {
            'role': role,
            'total_students': total_students,
            'total_teachers': total_teachers,
            'total_courses': total_courses,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
        }

        # بيانات إضافية للتشارت لكل دور
        if role in ['admin', 'teacher']:
            students = UserProfile.objects.filter(role='student')
            labels = [s.user.username for s in students]
            completed_per_student = [
                Submission.objects.filter(student=s.user, status='completed').count() for s in students
            ]
            pending_per_student = [
                Submission.objects.filter(student=s.user, status='pending').count() for s in students
            ]
            context.update({
                'students': students,
                'chart_labels': labels,
                'chart_completed': completed_per_student,
                'chart_pending': pending_per_student,
            })

        elif role == 'student':
            tasks = Task.objects.filter(assigned_to=user)
            context.update({'tasks': tasks})

        else:
            return HttpResponseForbidden("You are not authorized to view this page.")

        return render(request, 'dashboard/admin_dashboard.html' if role=='admin' else 'dashboard/dashboard.html', context)


# ==========================
# Unified Chart Data (AJAX) - JSON
# ==========================
@login_required
def dashboard_chart_data(request):
    user = request.user
    role = user.userprofile.role

    if role in ['admin', 'teacher']:
        students = UserProfile.objects.filter(role='student')
        labels = [s.user.username for s in students]
        completed = [Submission.objects.filter(student=s.user, status='completed').count() for s in students]
        pending = [Submission.objects.filter(student=s.user, status='pending').count() for s in students]

        data = {
            'labels': labels,
            'completed': completed,
            'pending': pending,
            'students': students.count(),
            'teachers': UserProfile.objects.filter(role='teacher').count(),
            'total_courses': Course.objects.count(),
            'total_tasks': Task.objects.count(),
            'completed_tasks': Submission.objects.filter(status='completed').count(),
            'pending_tasks': Submission.objects.filter(status='pending').count(),
        }

    elif role == 'student':
        data = {
            'completed': Submission.objects.filter(student=user, status='completed').count(),
            'pending': Submission.objects.filter(student=user, status='pending').count()
        }

    else:
        return HttpResponseForbidden()

    return JsonResponse(data)
