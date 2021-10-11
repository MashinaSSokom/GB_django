from django.shortcuts import render


def products(request):
    context = {'title': 'Каталог'}

    return render(request, 'products.html', context=context)
