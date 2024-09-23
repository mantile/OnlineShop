from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe

from .models import Product
from unfold.admin import ModelAdmin

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


@admin.register(Product)
class CustomAdminClass(ModelAdmin):
    list_display = ('short_name', 'short_description','image_display' , 'price', 'quantity')
    search_fields = ('name', 'description',)
    list_filter = ('name', 'description', 'price', 'quantity')

    def short_description(self, obj):
        return (obj.description[:100] + '...') if len(obj.description) > 100 else obj.description
    short_description.short_description = 'description'

    def short_name(self, obj):
        return (obj.name[:30] + '...') if len(obj.name) > 30 else obj.name
    short_name.short_name = 'name'

    def image_display(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: auto; height: 100px;"/>')  # Задайте размеры по вашему желанию
        return "Нет изображения"