from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from requests import request
from .models import CustomUser  # adjust the import if your model is in a different location
from .models import Inquiry
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.admin import AdminSite
from django.urls import reverse
from django.http import HttpResponseRedirect

class CustomAdminSite(AdminSite):
    def index(self, request, extra_context=None):
        return HttpResponseRedirect(reverse('admin:qusasa_customuser_changelist'))

admin_site = CustomAdminSite(name='custom_admin')

@admin.register(CustomUser)

class CustomUserAdmin(UserAdmin):
    # list_display defines which fields of the model will be displayed in the admin list view
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)

    # This defines the order in which fields will appear for user creation & modification
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # This redefines the 'add' form to suit your custom user model
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
        ),
    )

    # Defines the fields used by the search box of the admin interface
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)

admin_site.register(CustomUser, CustomUserAdmin)
