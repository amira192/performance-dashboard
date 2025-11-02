from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Submission, Feedback
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=Submission)
def notify_on_submission(sender, instance, created, **kwargs):
    if created:
        student = instance.student
        # email to managers? or student confirmation
        send_mail(
            subject=f"Submission received for {instance.task.title}",
            message=f"Your submission for '{instance.task.title}' was received at {instance.submission_date}.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            fail_silently=True
        )

@receiver(post_save, sender=Feedback)
def notify_on_feedback(sender, instance, created, **kwargs):
    if created:
        student = instance.submission.student
        send_mail(
            subject=f"New feedback for {instance.submission.task.title}",
            message=f"Manager {instance.manager.user.username} left feedback: {instance.comment}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[student.email],
            fail_silently=True
        )
