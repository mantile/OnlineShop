from django.db import models



class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True) #Add image
    quantity = models.PositiveIntegerField(default=0) #Add count

    def clean(self):
        if self.quantity < 0:
            raise ValueError({'quantity': 'cannot be a negative'})

    def save(self, *args, **kwargs):
        self.clean()  # Вызов валидации перед сохранением
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
