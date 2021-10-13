from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from profanity_filter import ProfanityFilter

from .models import *


@receiver(pre_save, sender=Post)
def del_special_char(sender, instance, **kwargs):
    """
    This signal delete special characters from title of post
    """
    # for example some special characters
    sp_chars = ['$', '&', '%', '^', '>', '<', '@', '~', '_', '|']
    title = instance.title
    instance.title = ''.join([str(ch) for ch in title if ch not in sp_chars])


@receiver(pre_save, sender=Comment)
def check_bad_words(sender, instance, **kwargs):
    """
    This signal changes profanity words in comments
    """
    pf = ProfanityFilter()
    text = instance.text
    instance.text = pf.censor(text)


@receiver(pre_delete, sender=Comment)
def reverse_delete(instance, **kwargs):
    """
    This signal prohibits the deletion of the comment.
    """
    if instance:
        raise TypeError(f"Don't delete comment for post {instance.post} ....")

