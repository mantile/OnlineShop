from django.db import models



class ProductType(models.Model):
    type_name = models.CharField(max_length=100, unique=True)

    def clean(self):
        # Проверка на существующие имена, если такое уже есть
        if ProductType.objects.filter(name=self.name).exists():
            raise ValidationError('Product type with this name already exists.')

    def __str__(self):
        return self.type_name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0) #Add count
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='products')

    def clean(self):
        if self.quantity < 0:
            raise ValueError({'quantity': 'cannot be a negative'})

    def save(self, *args, **kwargs):
        self.clean()  # Вызов валидации перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.product.name}"
