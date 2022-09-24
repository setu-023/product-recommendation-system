from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import CustomUser


class CustomeUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_type', 'email', 'password', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active')}
            ),
        )

admin.site.register(CustomUser, CustomeUserAdmin)