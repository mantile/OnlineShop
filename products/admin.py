from django.contrib import admin
from .models import Product

#Models import and registration
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity') #name and price to display
    search_fields = ('name',)