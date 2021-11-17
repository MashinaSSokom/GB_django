from django.contrib import admin
from . import models


@admin.register(models.ShopUser)
class ShopUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')


@admin.register(models.ShopUserProfile)
class ShopUserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')
