from django.db import models
from django.conf import settings

from mainapp.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SENT_TO_PROCEED = 'STP'
    PROCEEDED = 'PRD'
    PAID = 'PD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'Формируется'),
        (SENT_TO_PROCEED, 'Отправлен в обработку'),
        (PROCEEDED, 'Обработан'),
        (PAID, 'Оплачен'),
        (READY, 'Готов к выдаче'),
        (CANCEL, 'Отменен'),
    )

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)

    status = models.CharField(verbose_name='Статус', max_length=3, choices=ORDER_STATUS_CHOICES, default=FORMING)

    created = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Изменен', auto_now=True)

    is_active = models.BooleanField(verbose_name='Активность', default=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created']

    def __str__(self):
        return f'Заказ №{self.id}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_product_type_quantity(self):
        items = self.orderitems.select_related()
        return items.count()

    def get_total_cost(self):
        items = self.orderitems.select_related()

        return sum(list(map(lambda x: x.quantity * x.product.price, items)))

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()
        self.is_active = False
        self.save()

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }


class OrderItems(models.Model):
    order = models.ForeignKey(
        verbose_name='Заказ',
        to=Order,
        on_delete=models.CASCADE,
        related_name='orderitems'
    )

    product = models.ForeignKey(
        verbose_name='Продукт',
        to=Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)

    class Meta:
        verbose_name = 'Часть заказа'
        verbose_name_plural = 'Части заказа'
        ordering = ['-id']

    @staticmethod
    def get_item(id):
        return OrderItems.objects.filter(id=id).first()

    def get_product_cost(self):
        return self.quantity * self.product.price
