from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return (f'{self.name} \n '
                f'{self.description}')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    preview = models.ImageField(upload_to='catalog/', **NULLABLE, verbose_name='Изображение')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена за кв.м.')
    created_at = models.DateField(**NULLABLE, verbose_name='Дата создания')
    changed_at = models.DateField(**NULLABLE, verbose_name='Дата последнего изменения')

    def __str__(self):
        return f'{self.name} ({self.category})'


    def get_active_version(self):
        try:
            return self.version_set.get(version_tag=True)
        except Version.DoesNotExist:
            return None


    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    version_name = models.CharField(max_length=100, verbose_name='Название версии')
    version_number = models.IntegerField(verbose_name='Номер версии')
    version_tag = models.BooleanField(default=False, verbose_name='Признак текущей версии')

    def __str__(self):
        return f'{self.version_name} ({self.version_number})'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'


