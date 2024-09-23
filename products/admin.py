from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from django.utils.safestring import mark_safe
from django.shortcuts import render

from .models import Product, ProductType, ProductImage
from unfold.admin import ModelAdmin


admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Количество пустых форм для добавления новых изображений
    tab = True
    fields = ('image_preview', 'image', 'is_main')  # Отображаем изображение в качестве превью перед полем для загрузки
    readonly_fields = ('image_preview',)  # Делаем его только для чтения
    show_change_link = True

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: auto; height: 200px;"/>')
        return "Нет изображения"

    image_preview.short_description = 'Предпросмотр изображения'

    def save_related(self, request, formset, change, **kwargs): #Добавил **kwargs - исправление ошибки при сохранении
        super().save_related(request, formset, change, **kwargs)

        # Убедитесь, что только одно изображение является основным
        for form in formset:
            if form.cleaned_data.get('is_main'):
                # Если это изображение помечено как главное, удалим отметку у остальных
                ProductImage.objects.filter(product=form.instance, is_main=True).exclude(id=form.instance.id).update(is_main=False)


@admin.register(Product)
class CustomAdminClass(admin.ModelAdmin):
    inlines = [ProductImageInline]  # Включите ProductImage как inline в Product
    list_display = ('short_name', 'product_type', 'price', 'quantity')
    search_fields = ('name', 'product_type',)
    list_filter = ('name', 'product_type', 'price', 'quantity')

    def short_description(self, obj):
        return (obj.description[:100] + '...') if len(obj.description) > 100 else obj.description
    short_description.short_description = 'description'

    def short_name(self, obj):
        return (obj.name[:30] + '...') if len(obj.name) > 30 else obj.name
    short_name.short_name = 'name'



@admin.register(ProductType)
class CustomAdminClass(ModelAdmin):
    list_display = ('type_name', )
    search_fields = ('type_name', )