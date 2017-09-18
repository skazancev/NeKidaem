from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.db import models
from django.conf import settings
from django.template.loader import render_to_string


class PostManager(models.Manager):
    def get_queryset(self):
        return super(PostManager, self).get_queryset().order_by('-date')


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    objects = PostManager()

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def get_subscriber_emails(self):
        try:
            emails = self.user.subscribers.subscribers.values_list('email', flat=True)
        except Subscription.DoesNotExist:
            return []
        return list(filter(None, emails))

    def send_notification(self):
        site = Site.objects.get_current()
        html = render_to_string('blog/email/notification.txt', context={'post': self, 'site_url': site.domain})
        body = render_to_string('blog/email/notification.html', context={'post': self, 'site_url': site.domain})
        recipients = self.get_subscriber_emails()
        return send_mail(
            'Новый пост на %s' % site.name, body, settings.DEFAULT_FROM_EMAIL, recipients, html_message=html
        )


class Subscription(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='subscribers')
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscription')


class PostRead(models.Model):
    post = models.ForeignKey(Post, related_name='reads')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reads')

    class Meta:
        unique_together = ('post', 'user')
