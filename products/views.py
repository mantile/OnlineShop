from django.shortcuts import render
from .models import Product

def index(request):
    products = Product.objects.all()  # Получаем все продукты
    context = {
        'products': products,  # Передаем список продуктов в контекст
    }
    return render(request, 'products/index.html')
