from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

from .form import CustomUserCreationForm, CustomUserChangeForm
from .models import Address, Avatar, PhoneNumber

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address)
admin.site.register(Avatar)
admin.site.register(PhoneNumber)