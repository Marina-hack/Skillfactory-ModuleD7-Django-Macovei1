from celery import shared_task
from datetime import datetime, timedelta, time
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from unicodedata import category
from .models import Category, Subscription, Post
import time


@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


@shared_task
def with_every_new_post(category, preview, title, emails, get_absolute_url):
    """Вызывается в сигнале, при создании новой публикации и выполняет рассылку всем подписчикам категории."""

    subject = f'New at the category {category}'

    text_content = (
        f'Title: {title}\n'
        f'Preview: {preview}\n\n'  
        f'Link on a post: {settings.SITE_URL}{get_absolute_url}'
    )
    html_content = (
        f'Title: {title}<br>'
        f'Preview: {preview}<br><br>'
        f'<a href="{settings.SITE_URL}{get_absolute_url}">'
        f'Link on a post</a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def weekly_notification():
    today = datetime.utcnow()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(datetime_post_creation__gte=last_week)
    print(f'{posts}')
    users = User.objects.all().values_list('email', flat=True)
    categories = set(posts.values_list('category__name_category', flat=True))
    subscribers = set(Category.objects.filter(name_category__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'weekly_newsletter.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='weekly_newsletter',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()