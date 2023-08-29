from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, **NULLABLE, verbose_name='Слаг')
    content = models.TextField(**NULLABLE, verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/', **NULLABLE, verbose_name='Изображение')
    created_at = models.DateField(default=timezone.now, **NULLABLE, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.PositiveIntegerField(default=0, editable=False, verbose_name='Количество просмотров')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'запись'
        verbose_name_plural = 'записи'

