from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse

from mainapp.models import Product
from . import models


@login_required
def basket_view(request):
    basket = models.Basket.objects.filter(user=request.user)

    context = {'title': 'Корзина',
               'basket': basket}

    return render(request, 'basket.html', context)


@login_required
def basket_add_view(request, pk):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:detail_product', args=[pk]))

    product = get_object_or_404(Product, pk=pk)

    basket = models.Basket.objects.filter(user=request.user, product=product).first()

    if not basket:
        basket = models.Basket.objects.create(user=request.user, product=product)

    basket.quantity += 1
    basket.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_sub_view(request, pk):
    product = get_object_or_404(Product, pk=pk)

    basket = models.Basket.objects.filter(user=request.user, product=product).first()

    if basket.quantity > 1:
        basket.quantity -= 1
        basket.save()
    else:
        basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove_view(request, pk):
    basket = get_object_or_404(models.Basket, pk=pk)
    basket.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
