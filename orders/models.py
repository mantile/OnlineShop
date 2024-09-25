from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from users.models import Profile
from django.utils import timezone


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #user link Many TO One
    order_date = models.DateTimeField(auto_now_add=True) #Order date
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('complited', 'Complited'), ('canceled', 'Canceled')], default='pending')


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=50, decimal_places=2, editable=False)  # Цена за единицу
    total_price = models.DecimalField(max_digits=50, decimal_places=2, editable=False)  # Общая цена

    def save(self, *args, **kwargs):
        self.unit_price = self.product.price  # Используем цену из продукта
        self.total_price = self.unit_price * self.quantity  # Общая цена напрямую
        # Получаем основное изображение продукта
        main_image = self.product.images.filter(is_main=True).first()  # Получаем основное изображение
        if main_image:
            self.image = self.product.image  # Используйте основное изображение как нужно
        else:
            print("У продукта нет основного изображения.")
        super().save(*args, **kwargs)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(default=timezone.now)

    def add_item(self, product, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(product=product)
        if not created:
            cart_item.quantity += quantity
        cart_item.save()
        self.items.add(cart_item)

    def remove_item(self, cart_item):
        self.items.remove(cart_item)

    def total_price(self):
        return sum(item.subtotal() for item in self.items.all())

    def total_quantity(self):
        return sum(item.quantity for item in self.items.all())