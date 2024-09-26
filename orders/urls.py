from django.urls import path
from . import views
from .views import cart_view, update_cart_item_quantity, add_to_cart, create_order

app_name = 'orders'

urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', views.orders_view, name='orders'),
    path('cart/', cart_view, name='cart'),
    path('cart/update/<int:product_id>/', update_cart_item_quantity, name='update_cart_item'),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('create-order/', create_order, name='create_order'),
]