from django.urls import path
from . import views
from .views import product_list

app_name = 'products'  # Именование для включения URL

urlpatterns = [
    path('', product_list, name='product_list'),
]
