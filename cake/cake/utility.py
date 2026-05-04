import string

import random

from django.core.mail import EmailMultiAlternatives

from django.template.loader import render_to_string 

from decouple import config



def generate_password():

    password = ''.join(random.choices(string.ascii_letters+string.digits, k=8))

    return password


def send_email(subject,recipient,template,context):

    sender = config('EMAIL_HOST_USER')

    email_obj = EmailMultiAlternatives(subject,from_email=sender,to=[recipient])

    content = render_to_string(template,context)

    email_obj.attach_alternative(content,mimetype='text/html')

    email_obj.send()
