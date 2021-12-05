from django.db import models
from django.utils.functional import cached_property

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
    quantity = models.PositiveIntegerField(
        default=0
    )
    is_active = models.BooleanField(
        verbose_name='Активный', default=True
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
        return f'{self.product} {self.quantity} шт.'

    @cached_property
    def get_items_cashed(self):
        return self.user.basket.select_related()

    @property
    def get_full_product_price(self):
        return self.quantity*self.product.price

    @property
    def get_total_quantity(self):
        _total_products = self.get_items_cashed
        _totalquantity = sum(list(map(lambda x: x.quantity, _total_products)))
        return _totalquantity

    @property
    def get_total_price(self):
        _total_products = self.get_items_cashed
        _total_price = sum(list(map(lambda x: x.get_full_product_price, _total_products)))
        return _total_price

    @staticmethod
    def get_item(id):
        return Basket.objects.filter(id=id).first()
