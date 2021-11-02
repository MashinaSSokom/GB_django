from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryFrom
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render, reverse
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView
from django.db.models.query import QuerySet

from .forms import ProductFrom


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    title = 'админка/пользователи'

    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': title,
        'objects': users_list
    }

    return render(request, 'adminapp/user.html', context)


@user_passes_test(lambda u: u.is_superuser)
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
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    title = 'админка/редактировать пользователя'
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
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    title = 'админка/удалить пользователя'
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

    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_superuser)
def category_create(request):
    title = 'админка/создать категорию'

    if request.method == "POST":
        category_form = ProductCategoryFrom(data=request.POST)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))

    category_form = ProductCategoryFrom()

    context = {
        'title': title,
        'category_form': category_form
    }
    return render(request, 'adminapp/category_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_update(request, pk):
    title = 'админка/редактировать категорию'
    product_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == "POST":
        edit_form = ProductCategoryFrom(data=request.POST,
                                        instance=product_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))

    edit_form = ProductCategoryFrom(instance=product_category)

    context = {
        'title': title,
        'user_form': edit_form
    }
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    title = 'админка/удалить катеорию'
    product_category = get_object_or_404(ProductCategory, pk=pk)

    product_category.is_active = False
    product_category.save()

    return HttpResponseRedirect(reverse('admin_staff:categories'))


def product_create(request, pk):
    pass


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'adminapp/products.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['title'] = 'админка/продукты'
        return context

    def get_queryset(self: Product) -> QuerySet:
        queryset = super().get_queryset()
        category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
        return Product.objects.filter(category=category)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductFrom
    template_name = 'adminapp/product_update.html'

    def get_success_url(self):
        return reverse_lazy('admin_staff:products', kwargs={'pk': self.kwargs['pk']})

    def get_initial(self):
        return {'category': get_object_or_404(ProductCategory, pk=self.kwargs['pk'])}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data()
        context['title'] = 'админка/создать продукт'
        return context


    # def get_queryset(self: Product) -> QuerySet:
    #     queryset = super().get_queryset()
    #     category = get_object_or_404(ProductCategory, pk=self.kwargs['pk'])
    #     return Product.objects.filter(category=category)

def product_read(request, pk):
    pass


def product_update(request, pk):
    pass


def product_delete(request, pk):
    pass
