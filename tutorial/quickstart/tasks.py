from celery import shared_task

from .models import MyUser


@shared_task
def change_user_status(flag=False):
    list_users = MyUser.objects.filter(is_notified=flag).values_list('id', flat=True)
    flag = True if flag is False else False
    for user_id in list_users:
        user = MyUser.objects.get(pk=user_id)
        user.is_notified = flag
        user.save()

