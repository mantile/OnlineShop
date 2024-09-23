from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from users.models import Profile


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #user link Many TO One
    order_date = models.DateTimeField(auto_now_add=True) #Order date
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('complited', 'Complited'), ('canceled', 'Canceled')])


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
        if self.product.image:
            self.image = self.product.image
        super().save(*args, **kwargs)
