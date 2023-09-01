from django.conf import settings
import datetime
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.http import Http404

from .models import PostCategory, Post


def send_notifications(preview, pk, heading, subscribers):
    html_content = render_to_string(
        'post_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}'}
    )

    msg = EmailMultiAlternatives(
        subject=f'Новая статья!{heading}',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.post_category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.heading, subscribers_emails)


@receiver(pre_save, sender=Post)
def daily_posts_limit(sender, instance, **kwargs):
    user = instance.author.user
    today = datetime.datetime.now()
    count = Post.objects.filter(author__user=user, creation_datetime__date=today).count()
    print(count)
    if count > 3:
        raise Http404("Превышен лимит постов!")


@receiver(m2m_changed, sender=PostCategory)
def weekly_notify(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':

        categories = instance.post_category.all()
        subscribers_emails: list[str] = []
        for category in categories:
            subscribers_emails += category.subscribers.all()

            subscribers_emails = [s.email for s in subscribers_emails]

        send_notifications(instance.preview(), instance.pk, instance.heading, subscribers_emails)