from django.db.models.signals import post_save
from django.dispatch import receiver
from performance.models import Task
from .models import Notification
from django.contrib.auth.models import User

@receiver(post_save, sender=Task)
def notify_students(sender, instance, created, **kwargs):
    if created:
        students = User.objects.filter(userprofile__role='student')
        for student in students:
            Notification.objects.create(
                user=student,
                title=f"New Task: {instance.title}",
                message=f"A new task '{instance.title}' has been assigned to you."
            )
