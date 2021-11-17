
from django.urls import path

from .views import products_view, category_products_view, detail_product_view

app_name = 'mainapp'

urlpatterns = [
    path('page/<int:page>/', products_view, name='products'),
    path('category/<int:catid>/page/<int:page>/', category_products_view, name='product'),
    path('detail/<int:productid>', detail_product_view, name='detail_product'),
]
