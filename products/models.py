from django.db import models

#Firts model Product thats have a name, descr and price
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True) #Add image
    quantity = models.PositiveIntegerField(default=0) #Add count

    def __str__(self):
        return self.name
