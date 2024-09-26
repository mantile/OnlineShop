from django.shortcuts import render
from .models import Order, Cart, CartItem
from .models import Product, OrderItem
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
import json
from django.contrib.auth.decorators import login_required
from django.db import transaction

def index(request):
    return render(request, 'orders/index.html')

def orders_view(request):
    if request.user.is_authenticated:
        print(f"Пользователь: {request.user.username}")
        orders = Order.objects.filter(user=request.user).prefetch_related('items')
    else:
        print("Пользователь не аутентифицирован")
        orders = []

    return render(request, 'orders/orders.html', {'orders': orders})

def cart_view(request):
    cart = Cart.objects.first()
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
        cart, created = Cart.objects.get_or_create(id=1)
        cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
        if created:
            cart_item.quantity = 1
        else:
            cart_item.quantity += 1
        cart_item.save()
        total_quantity = cart.total_quantity()

        return JsonResponse({'success': True, 'total_quantity': total_quantity})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
def create_order(request):
    try:
        with transaction.atomic():
            if request.method == 'POST':
                print("Получил POST-запрос для создания заказа.")
                cart = get_object_or_404(Cart, user=request.user)
                if cart.items.count() == 0:
                    return JsonResponse({'success': False, 'message': 'Корзина пуста.'}, status=400)
                order = Order.objects.create(user=request.user)
                for cart_item in cart.items.all():
                    if not cart_item.product or not cart_item.quantity:
                        return JsonResponse({'success': False, 'message': 'Недопустимые данные в корзине.'}, status=400)
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        unit_price=cart_item.product.price
                    )
                order.update_total_order_price()  # Обновляем общую цену заказа
                cart.items.all().delete()  # Удаляем товары из корзины после оформления заказа

                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Неверный метод запроса.'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)