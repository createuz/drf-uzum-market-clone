from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(to_email, message, subject='Test subject', from_email='rajabovshohjahono3@gmail.com'):
    print(to_email)
    send_mail(
        subject,
        message,
        from_email,
        [to_email],
        fail_silently=True
    )
    return 'Done'