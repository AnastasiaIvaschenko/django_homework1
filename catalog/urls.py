from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import homepage, contacts, categories, category_facades

app_name = CatalogConfig.name

urlpatterns = [
    path('', homepage, name='homepage'),
    path('categories/', categories, name='categories'),
    path('<int:pk>/facades/', category_facades, name='category_facades'),
    path('contacts/', contacts),

]

