from django.contrib import admin
from . import models


@admin.register(models.ShopUser)
class FinishedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')
