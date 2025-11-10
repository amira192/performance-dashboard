from django.db.models.signals import post_save
from django.dispatch import receiver
from performance.models import Task, Submission
from .models import Notification

# add new task
@receiver(post_save, sender=Task)
def notify_new_task(sender, instance, created, **kwargs):
    if created:
        if instance.assigned_to:
            Notification.objects.create(
                user=instance.assigned_to,
                message=f"You have been assigned a new task: {instance.title}"
            )
# when task is reviewed
@receiver(post_save, sender=Submission)
def notify_task_review(sender, instance, created, **kwargs):
    if not created and instance.status == 'completed':
        Notification.objects.create(
            user=instance.student,
            message=f"Your submission for '{instance.task.title}' has been reviewed."
        )
