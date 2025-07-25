from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect

from .forms import SalesOrderForm, SalesOrderItemFormSet
from .models import Product, Customer, SalesOrder

from django.shortcuts import render

def home(request):
    return render(request, 'inventory/home.html',{'home':home})

def is_sales_exec(user):
    return user.role == 'sales_executive'


def is_manager_or_admin(user):
    return user.role in ['manager', 'admin']


@login_required
def product_list(request):
    #if not is_manager_or_admin(request.user):
    #    return HttpResponseForbidden()
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})


@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'inventory/customer_list.html', {'customers': customers})


@login_required
def sales_order_list(request):
    if is_sales_exec(request.user):
        orders = SalesOrder.objects.filter(created_by=request.user)
    else:
        orders = SalesOrder.objects.all()
    return render(request, 'inventory/sales_order_list.html', {'orders': orders})


@login_required
def create_sales_order(request):
    if request.method == 'POST':
        form = SalesOrderForm(request.POST)
        formset = SalesOrderItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()

            total = 0
            for item_form in formset:
                item = item_form.save(commit=False)
                item.sales_order = order

                if item.quantity > item.product.quantity:
                    messages.error(request, f"Insufficient stock for {item.product.name}")
                    order.delete()  # rollback
                    return redirect('create_sales_order')

                item.product.quantity -= item.quantity
                item.product.save()

                item.total_line_price = item.quantity * item.product.unit_price
                item.save()
                total += item.total_line_price

            order.total_amount = total
            order.save()

            messages.success(request, 'Sales order created successfully')
            return redirect('sales_order_list')
    else:
        form = SalesOrderForm()
        formset = SalesOrderItemFormSet()

    return render(request, 'inventory/create_sales_order.html', {'form': form, 'formset': formset})
