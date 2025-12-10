from django.db import models
from django.conf import settings


# Create your models here.
class Transactions(models.Model):
    transaction_id = models.CharField(max_length=100,blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    mpesa_receipt_number = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    

    def __str__(self):
        print( f"Transaction {self.mpesa_receipt_number} - {self.status} - {self.date_created}")
        return f"Transaction {self.mpesa_receipt_number} - {self.status} - {self.date_created}"
