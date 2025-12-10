from django.contrib import admin
from .models import Transactions




# Register your models here.
@admin.register(Transactions)
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ('mpesa_receipt_number', 'phone_number', 'amount', 'status', 'date_created')
    list_filter = ('status', 'transaction_id', 'date_created')
    search_fields = ('mpesa_receipt_number', 'phone_number', 'transaction_id', 'amount', 'status','date_created')
    