"""
Данный код определяет пользовательский фильтр censor для Django,
который заменяет часть нежелательных слов на символы *.
"""
from django import template

register = template.Library()

unwanted_words = ['Что-то', 'Новость3']

@register.filter()


def censor(value):

    if not isinstance(value, str):
        raise TypeError("Фильтр 'censor' может применяться только к строкам.")

    for words in unwanted_words:
        value = value.replace(words[1:], '*' * len(words[1:]))
    return value

