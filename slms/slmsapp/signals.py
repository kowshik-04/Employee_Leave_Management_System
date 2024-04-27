# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import LeaveRequest

@receiver(post_save, sender=LeaveRequest)
def send_leave_approval_email(sender, instance, created, **kwargs):
    if created:  # Only send email on new leave requests
        user_email = instance.staff_id.email
        subject = 'Leave Request Submitted'
        message = f'Your leave request from {instance.from_date} to {instance.to_date} has been submitted.'
        send_mail(subject, message, 'your_email@example.com', [user_email])
    else:  # Send disapproval email when status is updated to 2 (disapproved)
        if instance.status == 2:
            user_email = instance.staff_id.email
            subject = 'Leave Request Disapproved'
            message = f'Your leave request from {instance.from_date} to {instance.to_date} has been disapproved.'
            send_mail(subject, message, 'your_email@example.com', [user_email])
