from django.db import models
from django.contrib.auth import get_user_model
from pytils.translit import slugify

from . import settings


User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=80,
        verbose_name='Группа',
        help_text='Название группы',
    )
    slug = models.SlugField(
        max_length=30,
        unique=True,
        verbose_name='Короткий адрес',
        help_text='Короткий идентификатор группы',
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Текстовое описание группы',
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:settings.SLUG_MAX_LENGTH]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(
        verbose_name='Текст',
        help_text='Текстовое содержимое публикации',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        help_text='Дата публикации поста',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Имя создателя публикации',
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Имя группы для публикаций',
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.text[:settings.SELF_TEXT_LENGTH]
