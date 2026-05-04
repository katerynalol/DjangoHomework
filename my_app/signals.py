from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from my_app.models import Task
from django.contrib.auth import get_user_model


User = get_user_model()

@receiver(pre_save, sender=Task)
def store_old_status(sender, instance, **kwargs):
    if not instance.pk:
        instance._previous_status = None
        return

    try:
        old_instance = Task.objects.only('status').get(pk=instance.pk)
    except Task.DoesNotExist:
        instance._previous_status = None

    instance._previous_status = old_instance.status



@receiver(post_save, sender=Task)
def send_status_notification(sender, instance, created, **kwargs):
    if created:
        return

    old_status = instance._previous_status
    new_status = instance.status

    if not old_status or old_status == new_status:
        return

    owner = instance.owner

    if not owner or not owner.email:
        return

    subject = f'Статус задачи "{instance.title}" изменён'
    message = (
        f'Здравствуйте, {owner.username}!\n\n'
        f'Статус вашей задачи "{instance.title}" изменился:\n'
        f'  Было: {old_status}\n'
        f'  Стало: {new_status}'
    )

    send_mail(
        subject=subject,
        message=message,
        from_email='noreply@example.com',
        recipient_list=[owner.email],
        fail_silently=False,
    )