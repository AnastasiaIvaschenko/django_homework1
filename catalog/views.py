from django.shortcuts import render
from catalog.models import Category, Product


def homepage(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Главная'
    }
    return render(request, 'catalog/index2.html', context)

def categories(request):
    context = {
        'object_list': Category.objects.all(),
        'title': 'Каталог - наши фасады'
    }
    return render(request, 'catalog/categories.html', context)

def category_facades(request, pk):
    category_item = Category.objects.get(pk=pk)
    context = {
        'object_list': Product.objects.filter(category_id=pk),
        'title': f'Каталог - все наши фасады {category_item.name}'
    }
    return render(request, 'catalog/facades.html', context)


def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')
    return render(request, 'catalog/contacts1.html')



