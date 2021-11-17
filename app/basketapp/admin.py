from django.contrib import admin
from . import models


@admin.register(models.Basket)
class FinishedProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity',)

