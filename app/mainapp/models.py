from django.db import models


class ProductCategory(models.Model):
    """Модель категории продуктов"""

    name = models.CharField(
        verbose_name='Название',
        max_length=128
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
        verbose_name = 'Категория продуктов'
        verbose_name_plural = 'Категории продуктов'
        ordering = ['id']

    def __str__(self):
        return f'{self.name}'


class Product(models.Model):
    """Модель продукта"""

    category = models.ForeignKey(
        to=ProductCategory,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=120,
        unique=True
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='products_images',
        blank=True
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True
    )
    short_description = models.CharField(
        verbose_name='Краткое описание',
        max_length=40
    )
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=10,
        decimal_places=2
    )
    quantity = models.PositiveIntegerField(
        verbose_name='Количество на складе',
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
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['id']

    def __str__(self):
        return f'{self.name} ({self.category})'
