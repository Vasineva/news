"""
Данный код описывает форму PostForm, основанную на модели Post в рамках проекта Django.
- Поля формы:
- title: строковое поле для ввода заголовка поста, с ограничением в 128 символов
  и размещением надписи'Заголовок'.
- author: выбор автора из существующих в базе данных с подсказкой 'Выберите автора'.
- categories: возможность выбора нескольких категорий с использованием чекбоксов, с надписью 'Категория'.
- content: текстовое поле для содержания поста, требующее минимум 50 символов.

- Метод clean:
Этот метод отвечает за валидацию данных формы. Он проверяет, существует ли уже пост с таким
же заголовком и содержанием, и если да, генерирует ошибку валидации с сообщением о дубликате записи.

Форма используется для создания и редактирования постов в блоге, обеспечивая при этом
соблюдение уникальности заголовка и содержания.

"""
from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category, Author


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128, label='Заголовок')
    author = forms.ModelChoiceField(
        queryset=Author.objects.all(),
        label='Автор',
        empty_label='Выберите автора'
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Категория'
    )
    content = forms.CharField(min_length=50, label='Содержание', widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ['title', 'content', 'categories', 'author']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and content:
            existing_post = Post.objects.filter(
                title=title,
                content=content
            ).exists()

            if existing_post:
                raise ValidationError(
                    "Запись с таким заголовком и содержанием уже существует."
                )
        return cleaned_data
