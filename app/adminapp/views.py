from django.http import HttpResponseRedirect

from adminapp.forms import ShopUserAdminEditForm
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render, reverse
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'user.html', context)


def user_create(request):
    title = 'админка/создать пользователя'

    if request.method == "POST":
        user_form = ShopUserRegisterForm(data=request.POST,
                                         files=request.FILES)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))

    user_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'user_form': user_form
    }
    return render(request, 'user_update.html', context)


def user_update(request, pk):
    title = 'админка/редактирова пользователя'
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == "POST":
        edit_form = ShopUserAdminEditForm(data=request.POST,
                                          files=request.FILES,
                                          instance=user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:users'))

    edit_form = ShopUserAdminEditForm(instance=user)

    context = {
        'title': title,
        'user_form': edit_form
    }
    return render(request, 'user_update.html', context)


def user_delete(request, pk):
    title = 'админка/удалть пользователя'
    user = get_object_or_404(ShopUser, pk=pk)

    user.is_active = False
    user.save()

    return HttpResponseRedirect(reverse('admin_staff:users'))

@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'categories.html', content)


def category_create(request):
    pass


def category_update(request, pk):
    pass


def category_delete(request, pk):
    pass


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    content = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', content)


def product_create(request, pk):
    pass


def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass
