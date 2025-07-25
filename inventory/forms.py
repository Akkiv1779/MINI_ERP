from django import forms
from .models import SalesOrder, SalesOrderItem
from django.forms import inlineformset_factory

class SalesOrderForm(forms.ModelForm):
    class Meta:
        model = SalesOrder
        fields = ['order_number', 'customer']

SalesOrderItemFormSet = inlineformset_factory(
    SalesOrder,
    SalesOrderItem,
    fields=['product', 'quantity'],
    extra=1,
    can_delete=False
)
