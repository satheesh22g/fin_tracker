from django.db import models
from django.utils import timezone

class MainBalance(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

class Investment(models.Model):
    TYPE_CHOICES = [
        ('stock', 'Stock'),
        ('mf', 'Mutual Fund'),
        ('fd', 'Fixed Deposit'),
        ('rd', 'Recurring Deposit'),
    ]
    investment_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

class Lend(models.Model):
    lender_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

class UPIPayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)

class CreditCardPayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=timezone.now)
