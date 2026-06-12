import string

import random

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string 

from decouple import config

from app.models import Order



def generate_password():

    password = ''.join(random.choices(string.ascii_letters+string.digits, k=8))

    return password


def send_email(subject,recipient,template,context):

    sender = config('EMAIL_HOST_USER')

    email_obj = EmailMultiAlternatives(subject,from_email=sender,to=[recipient])

    content = render_to_string(template,context)

    email_obj.attach_alternative(content,mimetype='text/html')

    email_obj.send()



def generate_order_id():
    
    while True:

        order_id = 'KT-'+''.join(random.choices(string.digits,k=7))

        if not Order.objects.filter(order_id=order_id).exists():

            return order_id


def generate_otp():

    otp = ''.join(random.choices(string.digits,k=4))

    return otp