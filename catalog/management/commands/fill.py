from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product
# import json


class Command(BaseCommand):
    help = 'Заполнение базы данных новыми данными'

    def handle(self, *args, **options):

        # Удаляем все объекты модели из базы данных
        Product.objects.all().delete()
        Category.objects.all().delete()


        # Загружаем фикстуры
        call_command('loaddata', 'data.json')

        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена новыми данными'))

    # def handle(self, *args, **options):
    #     Product.objects.all().delete()
    #     Category.objects.all().delete()
    #     categories_list = []
    #     with open('data.json') as file:
    #         data = json.loads(file.read())
    #         for item in data:
    #             categories_list.append(item.get('fields'))
    #     categories_to_create = []
    #     products_to_create = []
    #     for item in categories_list:
    #         if not item.get('preview'):
    #             categories_to_create.append(Category(**item))
    #         else:
    #             products_to_create.append(Product(**item))
    #
    #     Category.objects.bulk_create(categories_to_create)
    #     Product.objects.bulk_create(products_to_create)

    # def handle(self, *args, **options):
    #     #удаление объектов из моделей
    #     Category.objects.all().delete()
    #     Product.objects.all().delete()
    #
    #     #загрузка данных из файла для модели Catalog
    #     with open('data.json') as f:
    #         data_category = json.load(f)
    #     category_list = []
    #     for category in data_category:
    #         category_id = category.get("pk")
    #         field = category.get('fields')
    #         name = field.get('name')
    #         description = field.get('description')
    #
    #         category_list.append(Category(name=name,
    #                                       description=description,
    #                                       pk=category_id))
    #
    #     #создание новых объектов в модели Catalog
    #     Category.objects.bulk_create(category_list)