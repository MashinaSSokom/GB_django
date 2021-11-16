from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import ListView, CreateView

from basketapp.models import Basket
from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItems
# Create your views here.


class OrderList(ListView):
    model = Order
    template_name = 'ordersapp/oreder_list.html'
    extra_context = {'title': 'Заказы'}

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(OrderList, self).get_context_data(**kwargs)
    #     context['title'] = 'Заказы'
    #     return context


class OrderCreate(CreateView):
    model = Order
    fields = []
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
                form.initial['quantity'] = basket_items[num].quantity_in_basket

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
        if self.object.get_total_cost() == 0:
            self.object.delete()

        return super(OrderCreate, self).form_valid(form)

