from django.db import models

# Create your models here.

from app.models import BaseClass

class PaymentStatusChoices(models.TextChoices):

    SUCCESS = 'Success','Success'

    PENDING ='Pending','Pending'

    FAILED = 'Failed','Failed'

class Payment(BaseClass):

    order = models.OneToOneField('app.Order',on_delete=models.CASCADE)

    amount = models.FloatField()

    payment_status = models.CharField(max_length=20,choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.PENDING)

    paid_at = models.DateTimeField(null=True,blank=True)

    class Meta :

        verbose_name = 'Payments'

        verbose_name_plural = 'Payments'

    def __str__(self):

        return f'{self.order.user.username}{self.order.order_id}Payment'
    
class Transaction(BaseClass):

    payment = models.ForeignKey('payment.Payment',on_delete=models.CASCADE)

    amount = models.FloatField()

    status = models.CharField(max_length=20,choices=PaymentStatusChoices.choices,default=PaymentStatusChoices.PENDING)

    rzp_order_id = models.SlugField()

    rzy_payment_id = models.SlugField(null=True,blank=True)

    rzy_signature = models.TextField(null=True,blank=True)

    transaction_at = models.DateTimeField(null=True,blank=True)

    class Meta :

        verbose_name = 'Transactions'

        verbose_name_plural = 'Transactions'

    def __str__(self):

        return f'{self.payment.order.user.username}{self.payment.order.order_id}Transactions'




