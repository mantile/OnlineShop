from django.shortcuts import render
from .models import Order, Cart, CartItem
from .models import Product
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
import json

def index(request):
    return render(request, 'orders/index.html')

def orders_view(request):
    if request.user.is_authenticated:
        print(f"Пользователь: {request.user.username}")  # Для отладки
        orders = Order.objects.filter(user=request.user).prefetch_related('items')
    else:
        print("Пользователь не аутентифицирован")  # Для отладки
        orders = []

    return render(request, 'orders/orders.html', {'orders': orders})

def cart_view(request):
    cart = Cart.objects.first()  # Получаем первую корзину, адаптируйте логику под пользователей
    return render(request, 'orders/cart.html', {'cart': cart})

def update_cart_item_quantity(request, product_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = data.get('quantity')
        cart_item = CartItem.objects.get(product_id=product_id)
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({'success': True, 'new_total_price': cart_item.subtotal()})

@require_POST
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(id=1)  # Замените на необходимую логику для получения корзины пользователя

        # Попробуем получить CartItem для этого продукта в корзине
        cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)

        if created:
            # Если товар только что создан, устанавливаем quantity на 1
            cart_item.quantity = 1
        else:
            # Если товар уже в корзине, увеличиваем quantity на 1
            cart_item.quantity += 1

        # Сохраняем изменения
        cart_item.save()

        # Получите общее количество товаров в корзине
        total_quantity = cart.total_quantity()  # Убедитесь, что эта функция правильно считает общее количество

        return JsonResponse({'success': True, 'total_quantity': total_quantity})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)