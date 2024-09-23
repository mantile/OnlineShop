from django.contrib import admin

from .models import Order, OrderItem
from unfold.admin import ModelAdmin
from products.models import Product
from django.utils.safestring import mark_safe


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'image_display', 'unit_price', 'quantity', 'total_price')  # Используем новые поля
    readonly_fields = ('unit_price', 'total_price', 'image_display')  # Оба поля только для чтения

    def image_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: auto; height: 100px;"/>')  # Задайте размеры по вашему желанию
        return "Нет изображения"

@admin.register(Order)
class CustomAdminClass(ModelAdmin):
    list_display = ('user', 'get_products', 'order_date', 'status')
    search_fields = ('user', 'order_date', 'status',)
    list_filter = ('user', 'order_date', 'status')
    inlines = [OrderItemInLine]

    def get_products(self, obj):
        return ', '.join([f'{item.product.name} x {item.quantity}' for item in obj.items.all()])

    get_products.short_descriptions = 'Product' # adnmin panel name
