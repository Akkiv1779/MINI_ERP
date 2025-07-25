from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('customers/', views.customer_list, name='customer_list'),
    path('orders/', views.sales_order_list, name='sales_order_list'),
    path('orders/create/', views.create_sales_order, name='create_sales_order'),
]