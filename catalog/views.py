from django.forms import inlineformset_factory
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView

from catalog.forms import ProductForm, VersionForm
from catalog.models import Category, Product, Version
from django.urls import reverse_lazy


def homepage(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Главная'
    }
    return render(request, 'catalog/index2.html', context)


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Все наши фасады'
    }


def product_list(request):
    products = Product.objects.all()
    context = {'object_list': products}
    return render(request, 'catalog/product_list.html', context)


class ProductsListView(ListView):
    model = Product

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)

        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk
        context_data['title'] = f'Каталог - все наши фасады {category_item.name}'
        return context_data


class ProductsCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:categories')


"""Класс Product является реализацией класса ProductsUpdateView, который расширяет класс UpdateView.
Он представляет собой представление для обновления объекта Product вместе со связанными 
с ним объектами Version с использованием набора форм."""
class ProductsUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:categories')
    '''Атрибут form_class определяет форму, которая будет использоваться для обновления экземпляра Product.'''
    '''Атрибут «success_url» указывает URL-адрес для перенаправления после успешной отправки формы. 
        В этом случае он использует функцию reverse_lazy для предоставления имени URL 
        для представления категорий в пространстве имен каталога.'''


    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data
    '''- Метод get_context_data переопределен для добавления набора форм к данным контекста.
        - `super().get_context_data(*args, **kwargs)` вызывает метод родительского класса 
        для получения исходных данных контекста.
        - `VersionFormset` генерируется с помощью функции `inlineformset_factory`, которая создает набор форм 
        для связи между моделями `Product` и `Version`. Аргумент form указывает форму, которая будет использоваться 
        для отдельных экземпляров формы в наборе форм.
        - Если метод HTTP — POST (указывающий отправку формы), набор форм связан с данными запроса и связан 
        с экземпляром Product. Если это запрос GET, набор форм связан с экземпляром Product без каких-либо данных.
        - Затем набор форм добавляется в словарь контекстных данных.'''
    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)
    '''— Метод form_valid переопределен для проверки формы и сохранения набора форм.
    - `formset` извлекается из контекстных данных, полученных с помощью `self.get_context_data()['formset']`.
    - Форма сохраняется, а экземпляр Product присваивается self.object.
    — Условие `if formset.is_valid()` проверяет корректность данных набора форм.
    - Если он действителен, экземпляр Product связан с набором форм с помощью formset.instance = self.object, 
    а затем набор форм сохраняется.
    - вызывается метод `super().form_valid(form)` для завершения обработки данных формы 
    и перенаправления на указанный `success_url`.'''

def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')
    return render(request, 'catalog/contacts1.html')



# def category_facades(request, pk):
#     category_item = Category.objects.get(pk=pk)
#     context = {
#         'object_list': Product.objects.filter(category_id=pk),
#         'title': f'Каталог - все наши фасады {category_item.name}'
#     }
