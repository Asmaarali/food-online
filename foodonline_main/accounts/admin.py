from django.contrib import admin
from .models import User , UserProfile
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomerUserAdmin(UserAdmin):
    # for password non editable field in admin
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    # for displaying fields in admin panel
    list_display = ["email", "first_name", "last_name", "username", "role", "is_active"]
    ordering = ["-date_joined"]


admin.site.register(User, CustomerUserAdmin)
admin.site.register(UserProfile)
