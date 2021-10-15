from django.shortcuts import render

from mainapp import models


def main(request):
    products = models.Product.objects.all()[:4]

    context = {
        'title': 'Главная',
        'products': products,
    }

    return render(request, 'index.html', context=context)


def contacts(request):
    context = {'title': 'Контакты'}

    return render(request, 'contacts.html', context=context)
