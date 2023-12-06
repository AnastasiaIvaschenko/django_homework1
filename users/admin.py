from django.contrib import admin
from users.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'phone', 'avatar', 'country', 'is_active', 'activation_token',)
