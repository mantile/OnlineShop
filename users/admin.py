from django.contrib import admin

from .models import Profile
from unfold.admin import ModelAdmin

@admin.register(Profile)
class CustomAdminClass(ModelAdmin):
    list_display = ('user', 'user_full_name', 'user_mail', 'address', 'phone_number')
    search_fields = ('user', 'phone_number', 'user_first_name', 'user_last_name', 'user_mail',)
    list_filter = ('user', 'phone_number')

    def user_full_name(self, obj):
        return f'{obj.user_last_name} {obj.user_first_name}'

    user_full_name.short_description = 'Full name'
