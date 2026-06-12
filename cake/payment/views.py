from django.shortcuts import render,redirect

# Create your views here.

from django.views import View

import razorpay

from decouple import config

from .models import Payment,Transaction

from django.utils import timezone

from django.contrib import messages

class RazorpaymentView(View):

    template = 'payment/razorpay.html'

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        payment = Payment.objects.get(uuid=uuid)

        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))

        data = { "amount": payment.amount*100, "currency": "INR", "receipt": "order_rcptid_11" }

        created_order = client.order.create(data=data)

        rzp_order_id = created_order.get('id')

        transaction = Transaction.objects.create(payment=payment,rzp_order_id=rzp_order_id,amount=payment.amount)

        data = {'RZP_CLIENT_ID':config('RZP_CLIENT_ID'),'amount':payment.amount,'order_id':rzp_order_id}

        return render(request,self.template,context=data)

class PaymentVerifyView(View):

    def post(self,request,*args,**kwargs):

        rzp_order_id = request.POST.get('razorpay_order_id')

        rzp_payment_id = request.POST.get('razorpay_payment_id')

        rzp_signature = request.POST.get('razorpay_signature')

        transaction = Transaction.objects.get(rzp_order_id=rzp_order_id)

        transaction.rzy_payment_id = rzp_payment_id

        transaction.rzy_signature = rzp_signature

        transaction.transaction_at =timezone.now()

        client = razorpay.Client(auth=(config('RZP_CLIENT_ID'), config('RZP_CLIENT_SECRET')))

        paid = client.utility.verify_payment_signature({
                                                'razorpay_order_id': rzp_order_id,
                                                'razorpay_payment_id': rzp_payment_id,
                                                'razorpay_signature': rzp_signature
                                                })
        
        if paid :

            transaction.status = 'Success'

            transaction.payment.payment_status = 'Success'

            transaction.payment.paid_at =timezone.now()

            transaction.payment.save()

            transaction.save()

            transaction.payment.order.user.cart.cakes.clear()

            messages.success(request,'Order Placed Successfully')

        else:

            transaction.status = 'Failed'

            transaction.save()

            messages.error(request,'Payment Failed!!')

        return redirect('home')
