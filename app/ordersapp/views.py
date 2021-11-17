from django.db import transaction
from django.db.models.signals import pre_save, pre_delete
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.dispatch import receiver

from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from basketapp.models import Basket
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItems


# Create your views here.


class OrderList(ListView):
    model = Order
    template_name = 'ordersapp/oreder_list.html'
    extra_context = {'title': 'Список заказов'}

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCreate(CreateView):
    model = Order
    fields = []
    extra_context = {'title': 'Заказ/создание'}
    template_name = 'ordersapp/order_form.html'
    success_url = reverse_lazy('orders:orders_list')

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        OrderFormSet = inlineformset_factory(Order, OrderItems, form=OrderItemForm, extra=1)

        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
            context['orderitems'] = formset
            return context

        basket_items = Basket.objects.filter(user=self.request.user)

        if len(basket_items):
            OrderFormSet = inlineformset_factory(Order, OrderItems, form=OrderItemForm, extra=len(basket_items))
            formset = OrderFormSet()

            for num, form in enumerate(formset.forms):
                form.initial['product'] = basket_items[num].product
                form.initial['quantity'] = basket_items[num].quantity
                form.initial['price'] = basket_items[num].product.price
            # basket_items.delete()
        else:
            formset = OrderFormSet()

        context['orderitems'] = formset
        context['basket'] = basket_items

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

        # удаляем пустой заказ
        print(self.object.get_total_cost())
        if self.object.get_total_cost() == 0:
            self.object.delete()

        basket_items = Basket.objects.filter(user=self.request.user)
        basket_items.delete()

        return super(OrderCreate, self).form_valid(form)


class OrderRead(DeleteView):
    model = Order
    extra_context = {'title': 'Заказ/просмотр'}
    template_name = 'ordersapp/order_detail.html'


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    order.status = Order.SENT_TO_PROCEED
    order.save()

    return HttpResponseRedirect(reverse('ordersapp:orders_list'))

# @receiver(signal=pre_delete, sender=OrderItems)
# @receiver(signal=pre_delete, sender=Basket)
# def product_quantity_update_save(sender, update_fields, instance, **kwargs):
#     if update_fields is 'quantity' or 'product':
#         if instance.id:
#             instance.product.quantity -= instance.quantity - sender.get_item(instance.id).quantity
#         else:
#             instance.product.quantity -= instance.quantity
#
#         instance.product.save()
#
#
# @receiver(signal=pre_save, sender=OrderItems)
# @receiver(signal=pre_save, sender=Basket)
# def product_quantity_update_delete(sender, instance, **kwargs):
#     instance.product.quantity += instance.quantity
#     instance.product.save()
