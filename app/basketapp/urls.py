
from django.urls import path

from .views import basket_view, basket_add_view, basket_remove_view, basket_sub_view

app_name = 'basketapp'

urlpatterns = [
    path('', basket_view, name='basket'),
    path('add/<int:pk>', basket_add_view, name='add'),
    path('sub/<int:pk>', basket_sub_view, name='sub'),
    path('remove/<int:pk>', basket_remove_view, name='remove'),
]
