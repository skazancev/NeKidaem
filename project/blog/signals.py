import threading

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from blog.models import Post, PostRead


@receiver(post_save, sender=Post)
def post_save_handler(sender, instance, created, **kwargs):
    if created:
        thread = threading.Thread(target=instance.send_notification)
        thread.start()
