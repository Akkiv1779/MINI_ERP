from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('sales_executive', 'Sales Executive'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sales_executive')


class Product(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Customer(models.Model):
    objects = None
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    gstin = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name


class SalesOrder(models.Model):
    objects = None
    order_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.order_number


class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    total_line_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.quantity > self.product.quantity:
                raise ValueError(f"Insufficient stock for product: {self.product.name}")
            self.product.quantity -= self.quantity
            self.product.save()
            self.total_line_price = self.product.unit_price * self.quantity
        super().save(*args, **kwargs)
