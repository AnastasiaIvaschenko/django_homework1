from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import homepage, contacts, CategoryListView, ProductsListView, ProductsCreateView, \
    ProductsUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', homepage, name='homepage'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('<int:pk>/facades/', ProductsListView.as_view(), name='category_facades'),
    path('<int:pk>/facades/create/', ProductsCreateView.as_view(), name='facade_create'),
    path('facades/<int:pk>/update/', ProductsUpdateView.as_view(), name='facade_update'),
    path('contacts/', contacts),

]

