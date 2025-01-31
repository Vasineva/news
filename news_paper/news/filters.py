"""
Данный код представляет собой класс фильтра для новостного приложения на Django,
использующего библиотеку django-filter.
"""
from django_filters import FilterSet, CharFilter, DateFilter
from django.forms.widgets import DateInput
from .models import Post

class NewsFilter(FilterSet):
    title = CharFilter(lookup_expr='icontains', label='Заголовок')
    author = CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Имя автора')
    created_at = DateFilter(
        lookup_expr='gt',
        widget=DateInput(attrs={'type': 'date'}), # Виджет для выбора даты.
        label='Дата публикации (позже)',
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'created_at']
