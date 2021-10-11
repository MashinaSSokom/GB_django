from django.shortcuts import render


def products(request):
    links_menu = [
        {'href': 'products', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    context = {'title': 'Каталог',
               'links_menu': links_menu}
    return render(request, 'products.html', context=context)
