
from django.urls import path

from .views import products, product

app_name = 'mainapp'

urlpatterns = [
    path('', products, name='products'),
    path('<int:pk>', product, name='product'),

]
