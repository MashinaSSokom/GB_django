from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import json
import os

from django.db import IntegrityError

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

JSON_PATH = 'mainapp/jsons/'


def load_from_json(name):
    with open(os.path.join(JSON_PATH, name+'.json'), 'r', encoding='utf-8') as f:
        return json.load(f)


class Command(BaseCommand):
    def handle(self, *args, **options):
        product_categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        for category in product_categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        for product in products:

            _product_category = ProductCategory.objects.get(name=product['category'])
            product['category'] = _product_category

            new_product = Product(**product)
            new_product.save()

        try:
            super_user = ShopUser.objects.create_superuser('admin', 'admin@admin.com', '123', age=25)
        except IntegrityError as e:
            print('Superuser already exists')
