from django.db import models

from authapp.models import ShopUser
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(
        to=ShopUser,
        on_delete=models.CASCADE,
        related_name='basket'
    )
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='product'
    )
    quantity_in_basket = models.PositiveIntegerField(
        default=0
    )
    created = models.DateField(
        auto_now_add=True
    )
    updated = models.DateField(
        auto_now=True
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['id']

    def __str__(self):
        return f'{self.product} {self.quantity_in_basket} шт.'

    def get_full_product_price(self):

        return self.quantity_in_basket*self.product.price
