from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import ListView
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib import messages
import csv
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from accounts.models import UserProfile
from .models import Task, Submission, Feedback, Course, Leave
from .forms import TaskForm, FeedbackForm, AddStudentForm, CourseForm, LeaveForm


# ==========================
# Dashboard
# ==========================
class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        role = request.user.userprofile.role
        notifications = request.user.notifications.order_by('-created_at')[:5]

        if role == 'admin':
            context = {
                'role': 'admin',
                'total_students': UserProfile.objects.filter(role='student').count(),
                'total_teachers': UserProfile.objects.filter(role='teacher').count(),
                'completed_tasks': Submission.objects.filter(status='completed').count(),
                'pending_tasks': Submission.objects.filter(status='pending').count(),
                'notifications': notifications,
            }
            template_name = 'dashboard/admin_dashboard.html'

        elif role == 'teacher':
            students = UserProfile.objects.filter(role='student')
            context = {
                'role': 'teacher',
                'students': students,
                'completed_tasks': Submission.objects.filter(status='completed').count(),
                'pending_tasks': Submission.objects.filter(status='pending').count(),
                'notifications': notifications,
            }
            template_name = 'dashboard/teacher_dashboard.html'

        elif role == 'student':
            student = request.user
            context = {
                'role': 'student',
                'completed': Submission.objects.filter(student=student, status='completed').count(),
                'pending': Submission.objects.filter(student=student, status='pending').count(),
                'tasks': Task.objects.filter(assigned_to=student),
                'notifications': notifications,
            }
            template_name = 'dashboard/student_dashboard.html'

        else:
            return HttpResponseForbidden("You are not authorized.")

        return render(request, template_name, context)


# ==========================
# Dashboard Chart Data
# ==========================
@login_required
def dashboard_chart_data(request):
    role = request.user.userprofile.role
    if role == 'admin':
        data = {
            'students': UserProfile.objects.filter(role='student').count(),
            'teachers': UserProfile.objects.filter(role='teacher').count(),
            'completed': Submission.objects.filter(status='completed').count(),
            'pending': Submission.objects.filter(status='pending').count(),
        }
    elif role == 'teacher':
        students = UserProfile.objects.filter(role='student')
        labels = [s.user.username for s in students]
        completed = [Submission.objects.filter(student=s.user, status='completed').count() for s in students]
        pending = [Submission.objects.filter(student=s.user, status='pending').count() for s in students]
        data = {'labels': labels, 'completed': completed, 'pending': pending}
    else:  # student
        student = request.user
        data = {
            'completed': Submission.objects.filter(student=student, status='completed').count(),
            'pending': Submission.objects.filter(student=student, status='pending').count()
        }
    return JsonResponse(data)



# Feedback Views

class FeedbackListView(LoginRequiredMixin, View):
    def get(self, request):
        role = request.user.userprofile.role

        if role == 'teacher' or role == 'admin':

            feedbacks = Feedback.objects.all()
        elif role == 'student':

            feedbacks = Feedback.objects.filter(student=request.user)
        else:
            return HttpResponseForbidden("Not authorized")

        return render(request, 'performance/feedback_list.html', {'feedbacks': feedbacks})



# Feedback Create (Only Teacher)
class FeedbackCreateView(LoginRequiredMixin, View):
    def get(self, request):

        if request.user.userprofile.role != 'teacher':
            return HttpResponseForbidden("Only teachers can give feedback")
        form = FeedbackForm()
        return render(request, 'performance/feedback_form.html', {'form': form})

    def post(self, request):
        if request.user.userprofile.role != 'teacher':
            return HttpResponseForbidden("Only teachers can give feedback")

        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.teacher = request.user
            feedback.save()
            messages.success(request, "Feedback added successfully")
            return redirect('feedback_list')

        return render(request, 'performance/feedback_form.html', {'form': form})




# Task Views

class TaskListView(ListView):
    model = Task
    template_name = 'performance/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 5

    def get_queryset(self):
        qs = Task.objects.all().order_by('-due_date')
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(title__icontains=query)
        return qs


def task_create(request):
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, "Task created successfully!")
        return redirect('task_list')
    return render(request, 'performance/task_form.html', {'form': form})


def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(request.POST or None, instance=task)
    if form.is_valid():
        form.save()
        messages.success(request, "Task updated successfully!")
        return redirect('task_list')
    return render(request, 'performance/task_form.html', {'form': form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('task_list')
    return render(request, 'performance/task_confirm_delete.html', {'task': task})


def export_tasks_csv(request):
    tasks = Task.objects.all()
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tasks.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Status', 'Due Date', 'Assigned To'])
    for t in tasks:
        writer.writerow([t.title, t.description, t.status, t.due_date, t.assigned_to.username if t.assigned_to else 'Unassigned'])
    return response



# Student Views

class AddStudentView(LoginRequiredMixin, View):
    def get(self, request):
        form = AddStudentForm()
        return render(request, 'performance/add_student.html', {'form': form})

    def post(self, request):
        form = AddStudentForm(request.POST)
        if form.is_valid():
            student_profile = form.save(commit=False)
            student_profile.role = 'student'
            student_profile.save()
            messages.success(request, "Student added successfully!")
            return redirect('add_student')
        return render(request, 'performance/add_student.html', {'form': form})



# Course Views

class AddCourseView(LoginRequiredMixin, View):
    def get(self, request):
        form = CourseForm()
        return render(request, 'performance/add_course.html', {'form': form})

    def post(self, request):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully!")
            return redirect('add_course')
        return render(request, 'performance/add_course.html', {'form': form})



# Leave Views

class LeaveListView(LoginRequiredMixin, View):
    def get(self, request):
        role = request.user.userprofile.role
        leaves = Leave.objects.filter(student=request.user) if role == 'student' else Leave.objects.all()
        return render(request, 'performance/leave_list.html', {'leaves': leaves})


class LeaveCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = LeaveForm()
        return render(request, 'performance/leave_form.html', {'form': form})

    def post(self, request):
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            if request.user.userprofile.role == 'student':
                leave.student = request.user
            leave.save()
            messages.success(request, "Leave request submitted successfully!")
            return redirect('leave_list')
        return render(request, 'performance/leave_form.html', {'form': form})
