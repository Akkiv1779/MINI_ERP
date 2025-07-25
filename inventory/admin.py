from django.contrib import admin
from .models import User, Product, Customer, SalesOrder, SalesOrderItem

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(SalesOrder)
admin.site.register(SalesOrderItem)