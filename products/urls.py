from django.urls import path
from . import views

app_name = 'products'  # Именование для включения URL

urlpatterns = [
    path('', views.index, name='index'),
]
