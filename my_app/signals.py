from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from my_app.models import Task
from django.contrib.auth import get_user_model


User = get_user_model()

@receiver(pre_save, sender=Task)
def send_status_notification(sender, instance, created, **kwargs):
    if created:
        return

    if not hasattr(instance, '_old_status'):
        return

    old_status = instance._old_status
    new_status = instance.status

    if not old_status or old_status == new_status:
        return

    owner = instance.owner
    if not owner or not owner.email:
        return


    subject = f'Статус задачи "{instance.title}" изменён'
    message = (
        f'Здравствуйте, {owner.get_full_name() or owner.username}!\n\n'
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