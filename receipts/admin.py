from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Receipt, User
from preferences.models import OrderingPreference

# Register your models here.
class Admin(UserAdmin):
    model = User
    list_display = ['email', 'username', ]


admin.site.register(Receipt)
admin.site.register(OrderingPreference)

