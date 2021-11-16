from django.urls import path

from ordersapp import views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    # path('page/<int:page>/', products_view, name='products'),
    path('', ordersapp.OrderList.as_view(), name='orders_list'),
    # path('forming/complete/<int:pk>/', ordersapp.order_forming_complete, name='order_forming_complete'),
    path('create/', ordersapp.OrderCreate.as_view(), name='order_create'),
    # path('read/<int:pk>/', ordersapp.OrderRead.as_view(), name='order_read'),
    # path('update/<int:pk>/', ordersapp.OrderItemsUpdate.as_view(), name='order_update'),
    # path('delete/<int:pk>/', ordersapp.OrderDelete.as_view(), name='order_delete'),

]
