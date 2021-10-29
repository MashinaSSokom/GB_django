
from django.urls import path

from .views import products_view, category_products_view, detail_product_view

app_name = 'mainapp'

urlpatterns = [
    path('', products_view, name='products'),
    path('category/<int:catid>', category_products_view, name='product'),
    path('detail/<int:productid>', detail_product_view, name='detail_product'),
]
