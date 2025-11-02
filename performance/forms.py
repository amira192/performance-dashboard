from django import forms
from .models import Task, Submission, Feedback

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'due_date', 'assigned_to']

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['task', 'content', 'status']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['student', 'comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'rows':3}),
            'rating': forms.NumberInput(attrs={'min':0, 'max':5})
        }
