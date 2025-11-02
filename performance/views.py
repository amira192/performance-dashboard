from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import HttpResponse, HttpResponseForbidden
from .models import Task, Submission, Feedback
from .forms import TaskForm, SubmissionForm, FeedbackForm
from accounts.models import UserProfile
from django.views.generic import ListView
import csv

# ---------------- Dashboard Views ----------------
class AdminDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.userprofile.role != 'admin':
            return HttpResponseForbidden("You are not authorized.")
        total_students = UserProfile.objects.filter(role='student').count()
        total_managers = UserProfile.objects.filter(role='manager').count()
        pending_tasks = Task.objects.filter(status='pending').count()
        context = {
            'total_students': total_students,
            'total_managers': total_managers,
            'pending_tasks': pending_tasks
        }
        return render(request, 'dashboard/admin_dashboard.html', context)


class ManagerDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.userprofile.role != 'manager':
            return HttpResponseForbidden("You are not authorized.")
        students = UserProfile.objects.filter(role='student')
        return render(request, 'dashboard/manager_dashboard.html', {'students': students})


class StudentDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.userprofile.role != 'student':
            return HttpResponseForbidden("You are not authorized.")
        submissions = Submission.objects.filter(student=request.user)
        return render(request, 'dashboard/student_dashboard.html', {'submissions': submissions})


# ---------------- Feedback Views ----------------
class FeedbackListView(LoginRequiredMixin, View):
    def get(self, request):
        role = request.user.userprofile.role
        if role not in ['admin', 'manager']:
            return HttpResponseForbidden("You are not authorized.")
        if role == 'admin':
            feedbacks = Feedback.objects.all()
        else:  # manager
            feedbacks = Feedback.objects.filter(student__userprofile__supervisor=request.user)
        return render(request, 'performance/feedback_list.html', {'feedbacks': feedbacks})


class FeedbackCreateView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.userprofile.role not in ['admin', 'manager']:
            return HttpResponseForbidden("You are not authorized.")
        form = FeedbackForm()
        return render(request, 'performance/feedback_form.html', {'form': form})

    def post(self, request):
        if request.user.userprofile.role not in ['admin', 'manager']:
            return HttpResponseForbidden("You are not authorized.")
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.manager = request.user
            feedback.save()
            return redirect('feedback_list')
        return render(request, 'performance/feedback_form.html', {'form': form})


# ---------------- Task Views ----------------
class TaskListView(ListView):
    model = Task
    template_name = 'performance/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        qs = Task.objects.all().order_by('-due_date')
        if query:
            qs = qs.filter(title__icontains=query)
        return qs


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'performance/task_form.html', {'form': form})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'performance/task_form.html', {'form': form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'performance/task_confirm_delete.html', {'task': task})


def export_tasks_csv(request):
    tasks = Task.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Status', 'Due Date', 'Assigned To'])
    for task in tasks:
        writer.writerow([task.title, task.description, task.status, task.due_date, task.assigned_to.username if task.assigned_to else 'Unassigned'])
    return response
