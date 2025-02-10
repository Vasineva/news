from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
from datetime import timedelta
from django.utils.timezone import now

@shared_task
def send_new_post_notifications(post_id):
    post = Post.objects.get(id=post_id)
    categories = post.categories.all()

    for category in categories:
        subscribers = category.subscribers.all()
        if subscribers.exists():
            for subscriber in subscribers:
                html_content = render_to_string(
                    'post/post_created.html',
                    {
                        'post': post,
                        'post_url': f"http://127.0.0.1:8000/posts/{post.id}"
                    }
                )
                msg = EmailMultiAlternatives(
                    subject=f"Новая публикация в категории: {category.name}",
                    body=f'Здравствуйте! В категории "{category.name}", на которую вы подписаны, появилась новая публикация!\n{post.content[:50]}',
                    from_email='vasinevakatirina@yandex.ru',
                    to=[subscriber.email]
                )
                msg.attach_alternative(html_content, 'text/html')
                msg.send()

@shared_task
def send_weekly_digest():
    """Еженедельная рассылка новостей подписчикам."""
    week_ago = now() - timedelta(days=7)

    for category in Category.objects.all():
        posts = Post.objects.filter(categories=category, created_at__gte=week_ago)

        if posts.exists():
            subscribers = category.subscribers.all()
            for subscriber in subscribers:
                html_content = render_to_string(
                    'weekly_subscription.html',
                    {
                        'posts': posts,
                        'subscriber': subscriber,
                        'category': category,
                    }
                )

                subject = f"Еженедельная подборка постов в категории: {category.name}"
                text_content = "\n".join(
                    [f"{post.title}: http://127.0.0.1:8000/posts/{post.id}" for post in posts]
                )

                msg = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email='vasinevakatirina@yandex.ru',
                    to=[subscriber.email],
                )
                msg.attach_alternative(html_content, "text/html")
                msg.send()