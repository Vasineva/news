from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache

article = 'AR'
news = 'NW'

POST_TYPES = [
    (article, 'Статья'),
    (news, 'Новость')
]

# Модель Author
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author_profile")
    rating = models.IntegerField(default=0)

    def __str__(self):
        # Возвращаем имя пользователя, связанного с автором
        return self.user.username



    def update_rating(self):
        # Суммарный рейтинг статей автора * 3
        post_ratings = sum(post.rating for post in self.posts.all()) * 3

        # Суммарный рейтинг всех комментариев автора
        comment_ratings = sum(comment.rating for comment in self.user.user_comments.all())

        # Суммарный рейтинг всех комментариев к статьям автора
        post_comment_ratings = sum(
            comment.rating for post in self.posts.all() for comment in post.comments.all()
        )

        # Обновляем рейтинг
        self.rating = post_ratings + comment_ratings + post_comment_ratings
        self.save()


# Модель Category
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, related_name='subscribers')

    def __str__(self):
        return self.name


# Модель Post
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="posts")
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=article)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory', related_name="posts")
    title = models.CharField(max_length=128)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    # предварительный просмотр
    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

# Промежуточная модель для связи «многие ко многим»
class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='post_categories')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='category_posts')

# Модель Comment
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()