from django.db.models.signals import pre_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import PostCategory

@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.categories.all()

        for category in categories:
            subscribers = category.subscribers.all()
            if subscribers.exists():
                for subscriber in subscribers:
                    html_content = render_to_string(
                        'post/post_created.html',
                        {
                            'post': instance,
                            'post_url': f"http://127.0.0.1:8000/posts/{instance.id}"
                         }
                    )
                    post_heading = instance.title
                    msg = EmailMultiAlternatives(
                        subject=f"Новая публикация в категории: {post_heading}",
                        body=f'Здравствуйте! В категории "{category.name}", на которую вы подписаны, появилась новая публикация!\n{instance.content[:50]}',
                        from_email='vasinevakatirina@yandex.ru',
                        to=[subscriber.email]
                    )
                    msg.attach_alternative(html_content, 'text/html')
                    msg.send()