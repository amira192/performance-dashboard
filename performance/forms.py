from django import forms
from django.contrib.auth.models import User
from .models import Task, Feedback, Course, Leave
from accounts.models import UserProfile
from django.utils import timezone

# ---------------- Task Form ----------------
class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
        required=True,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border p-2 rounded w-full'})
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date', 'assigned_to']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border p-2 rounded w-full', 'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'class': 'border p-2 rounded w-full', 'rows': 4, 'placeholder': 'Task Description'}),
            'status': forms.Select(attrs={'class': 'border p-2 rounded w-full'}),
            'assigned_to': forms.Select(attrs={'class': 'border p-2 rounded w-full'}),
        }

# ---------------- Feedback Form ----------------
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['student', 'comment', 'rating']
        widgets = {
            'student': forms.Select(attrs={'class': 'border p-2 rounded w-full'}),
            'comment': forms.Textarea(attrs={'class': 'border p-2 rounded w-full', 'rows': 4, 'placeholder': 'Enter feedback here...'}),
            'rating': forms.NumberInput(attrs={'class': 'border p-2 rounded w-full', 'min': 0, 'max': 10}),
        }

# ---------------- Course Form ----------------
class CourseForm(forms.ModelForm):
    start_date = forms.DateField(
        required=True,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border p-2 rounded w-full'})
    )
    end_date = forms.DateField(
        required=True,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border p-2 rounded w-full'})
    )

    class Meta:
        model = Course
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'border p-2 rounded w-full', 'placeholder': 'Course Title'}),
            'description': forms.Textarea(attrs={'class': 'border p-2 rounded w-full', 'rows': 4, 'placeholder': 'Course Description'}),
        }


# ---------------- Leave Form ----------------
class LeaveForm(forms.ModelForm):
    start_date = forms.DateField(
        required=True,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border p-2 rounded w-full'})
    )
    end_date = forms.DateField(
        required=True,
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'border p-2 rounded w-full'})
    )

    class Meta:
        model = Leave
        fields = ['leave_type', 'start_date', 'end_date', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'class': 'border p-2 rounded w-full', 'rows': 3}),
        }


# ---------------- Add Student Form ----------------
class AddStudentForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Users without UserProfile can be added
        self.fields['user'].queryset = User.objects.filter(userprofile__isnull=True)
        self.fields['user'].label = "Select User to Add as Student"
