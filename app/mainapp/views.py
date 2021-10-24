from django.shortcuts import render, get_object_or_404
import json

from . import models


def detail_product_view(request, catid, productid):

    detail_product = models.Product.objects.filter(category_id=catid).filter(id=productid)[0]

    links_menu = models.ProductCategory.objects.all()
    category = get_object_or_404(models.ProductCategory, id=catid)
    related_products = models.Product.objects.filter(category_id=catid).exclude(id=productid)

    context = {'title': 'Каталог',
               'detail_product': detail_product,
               'links_menu': links_menu,
               'category': category,
               'related_products': related_products}
    return render(request, 'detail.html', context=context)


def category_products_view(request, catid):
    links_menu = models.ProductCategory.objects.all()
    category = get_object_or_404(models.ProductCategory, id=catid)
    products = models.Product.objects.filter(category_id=catid)

    context = {'title': 'Каталог',
               'links_menu': links_menu,
               'category': category,
               'products': products}
    return render(request, 'products.html', context=context)


def products_view(request):
    links_menu = models.ProductCategory.objects.all()

    products = models.Product.objects.all()

    context = {'title': 'Каталог',
               'links_menu': links_menu,
               'products': products}

    return render(request, 'products.html', context=context)
