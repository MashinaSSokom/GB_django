from django.contrib import admin
from . import models


@admin.register(models.ProductCategory)
class FinishedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'updated',)


@admin.register(models.Product)
class FinishedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'updated',)
