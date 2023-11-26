from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView
from catalog.forms import ProductForm
from catalog.models import Category, Product
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


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


# def category_facades(request, pk):
#     category_item = Category.objects.get(pk=pk)
#     context = {
#         'object_list': Product.objects.filter(category_id=pk),
#         'title': f'Каталог - все наши фасады {category_item.name}'
#     }

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


class ProductsCreateView(LoginRequiredMixin, CreateView):
    login_url = 'users/login/'
    redirect_field_name = 'login.html'

    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:categories')

    def form_valid(self, form):
        self.object = form.save()
        self.object.designer = self.request.user
        self.object.save()
        return super().form_valid(form)


class ProductsUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'users/login/'
    redirect_field_name = 'login.html'
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:categories')



def contacts(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        print(f'{name} ({email}): {message}')
    return render(request, 'catalog/contacts1.html')



