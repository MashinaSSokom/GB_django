from django.shortcuts import render
import json

from . import models


def products(request):
    links_menu = models.ProductCategory.objects.all()

    related_products = models.Product.objects.all()[:4]
    # with open(r'F:\projects\GB_django\app\products.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)
    #     for v in data.values():
    #         related_products.append(v)

    context = {'title': 'Каталог',
               'links_menu': links_menu,
               'related_products': related_products}
    return render(request, 'products.html', context=context)
