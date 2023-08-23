from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import homepage, contacts, CategoryListView, ProductsListView

app_name = CatalogConfig.name

urlpatterns = [
    path('', homepage, name='homepage'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('<int:pk>/facades/', ProductsListView.as_view(), name='category_facades'),
    path('contacts/', contacts),

]

