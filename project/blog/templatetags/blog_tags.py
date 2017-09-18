from django import template

from blog.models import Subscription, PostRead

register = template.Library()


@register.filter
def is_subscribed(user, target):
    try:
        return user in target.subscribers.subscribers.all()
    except Subscription.DoesNotExist:
        return False


@register.filter
def is_read(post, user):
    try:
        PostRead.objects.get(user_id=user, post_id=post)
        return True
    except PostRead.DoesNotExist:
        return False


@register.filter
def get_read(user):
    return PostRead.objects.filter(user_id=user).values_list('post_id', flat=True)
