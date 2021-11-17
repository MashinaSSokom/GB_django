from mainapp.models import ProductCategory


def links_menu(request):
    links_menu = ProductCategory.objects.all()

    return {
        'links_menu': links_menu
    }
