from django.shortcuts import render
import json

def products(request):
    links_menu = [
        {'href': 'products', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]

    related_products = []
    with open(r'F:\projects\GB_django\app\products.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        for v in data.values():
            related_products.append(v)

    context = {'title': 'Каталог',
               'links_menu': links_menu,
               'related_products': related_products}
    return render(request, 'products.html', context=context)
