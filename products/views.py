from django.shortcuts import render
from .models import Product

def index(request):
    products = Product.objects.all()  # Получаем все продукты
    context = {
        'products': products,  # Передаем список продуктов в контекст
    }
    return render(request, 'products/index.html', {'products': products})

def product_list(request):
    products = Product.objects.all()  # Получаем все продукты
    products_with_main_image = []

    for product in products:
        main_image = product.images.filter(is_main=True).first()  # Получаем главное изображение
        products_with_main_image.append((product, main_image))  # Добавляем кортеж (продукт, главное изображение)

    #print(f"Found {len(products_with_main_image)} products")  # Вывод количества продуктов
    return render(request, 'products/index.html', {
        'products_with_main_image': products_with_main_image,  # Передаём в шаблон
    })