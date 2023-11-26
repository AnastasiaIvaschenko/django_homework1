from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Заполнение базы данных новыми данными'

    def handle(self, *args, **options):

        # Удаляем все объекты модели из базы данных
        Product.objects.all().delete()
        Category.objects.all().delete()


        # Загружаем фикстуры
        call_command('loaddata', 'data.json')

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена новыми данными'))
