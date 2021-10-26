from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from mainapp.models import Product
from . import models


def basket_view(request):
    basket = models.Basket.objects.filter(user=request.user)

    context = {'title': 'Корзина',
               'basket': basket}

    return render(request, 'basket.html', context)


def basket_add_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = models.Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = models.Basket.objects.create(user=request.user, product=product)

    basket.quantity_in_basket += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def basket_remove_view(request, pk):
    # basket = models.Basket.objects.filter(product=product).first()
    #
    # if not basket:
    #     models.Basket.objects.create(product=product)
    #
    # basket.quantity_in_basket += 1
    # basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
