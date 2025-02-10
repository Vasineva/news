from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment, article, news

#  Создать двух пользователей
user1 = User.objects.create_user('Екатерина', password='0000')
user2 = User.objects.create_user('Юлия', password='1111')
user3 = User.objects.create_user('Марина', password='2222')
user4 = User.objects.create_user('Оля', password='3333')
user5 = User.objects.create_user('Женя', password='4444')

#  Создать два объекта модели Author, связанные с пользователями
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)
author3 = Author.objects.create(user=user3)
author4 = Author.objects.create(user=user4)
author5 = Author.objects.create(user=user5)

#  Добавить 4 категории в модель Category
cat1 = Category.objects.create(name='Здоровье')
cat2 = Category.objects.create(name='Техника')
cat3 = Category.objects.create(name='Наука')
cat4 = Category.objects.create(name='Еда')
cat5 = Category.objects.create(name='Что-то')


#  Добавить 2 статьи и 1 новость
post1 = Post.objects.create(author=author1, post_type=article, title="Срок службы", content="Срок службы моего ноутбука подходит к концу.")
post2 = Post.objects.create(author=author1, title="Испортился новогодний салат.", content="Всеми хозяйками России было доказано, что слишком большое количество приготовленных салатов на новый год грозит к неизбежной порчи большого количества из них (спасутся только любимые). Решение данной проблемы в том чтобы готовить по одному любимому салату на члена семьи.")
post3 = Post.objects.create(author=author2, post_type=news, title="Сон", content="Учеными доказано, что сон должен быть более 8 часов.")
post4 = Post.objects.create(author=author3, post_type=news, title="Новость2", content="Что-то случилось 2.")
post5 = Post.objects.create(author=author1, post_type=news, title="Новость3", content="Что-то случилось 3.")
post6 = Post.objects.create(author=author4, post_type=news, title="Новость3", content="Что-то слууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууууучилось 3.")
post7 = Post.objects.create(author=author5, post_type=news, title="Новость4", content=" Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3. Что-то случилось 3.")


#  Присвоить им категории
post1.categories.add(cat2, cat3)
post2.categories.add(cat4)
post3.categories.add(cat3, cat1)
post4.categories.add(cat4, cat1, cat5)

# Создать как минимум 4 комментария
comment1 = Comment.objects.create(post=post1, user=user2, text="Жаль!")
comment2 = Comment.objects.create(post=post2, user=user1, text="А я так и делаю!")
comment3 = Comment.objects.create(post=post3, user=user1, text="Отлично.")
comment4 = Comment.objects.create(post=post3, user=user2, text="Очень важная информация.")

# like() и dislike() к статьям/новостям и комментариям
post1.like()
post2.like()
post2.dislike()
post3.dislike()
post3.like()

comment1.like()
comment1.like()
comment2.like()
comment3.dislike()
comment4.like()

# Обновить рейтинги пользователей
author1.update_rating()
author2.update_rating()

# Вывести username и рейтинг лучшего пользователя
best_author = Author.objects.order_by('-rating').first()
f"Лучший автор: {best_author.user.username}, Рейтинг: {best_author.rating}"

# Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи
best_post = Post.objects.order_by('-rating').first()
f"Дата: {best_post.created_at}, Автор: {best_post.author.user.username}, Рейтинг: {best_post.rating}, Заголовок: {best_post.title}, Превью: {best_post.preview()}"

# Вывести все комментарии к этой статье
comments = best_post.comments.all()
for comment in comments:
    f"Дата: {comment.created_at}, Пользователь: {comment.user.username}, Рейтинг: {comment.rating}, Комментарий: {comment.text}"

# вывисти всех авторов сразу
Category = Category.objects.all()

#вывисти одного автора
Author.objects.get(id=2)