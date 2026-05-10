from django.shortcuts import render, redirect

# Create your views here.

from django.views import View

from .forms import LoginForm , RegisterForm

from django.contrib.auth import authenticate, login , logout

from cake.utility import generate_password , send_email

from django.contrib.auth.hashers import make_password

from decouple import config

import threading

from app.models import Wishlist,Cart

from django.db import transaction


class LoginView(View):

    template = 'authentication/login.html'

    form_class = LoginForm

    page = 'Login'

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form}

        return render(request,self.template,context=data)
    


    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            email = form.cleaned_data.get('email')

            password = form.cleaned_data.get('password')

            user =authenticate(username=email,password=password)

            if user :

                login(request,user)

                return redirect('home')
            
            error = 'Invalid Credentials'
            

        data = {'form':form,'page':self.page,'error':error}

        return render(request,self.template,context=data)
    

class LogoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('home')
    

class RegisterView(View):

    template = 'authentication/register.html'

    form_class = RegisterForm

    page = 'Signup'

    def get (self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form,'page':self.page}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            with transaction.atomic():

                user= form.save(commit=False)

                email= form.cleaned_data.get('email')

                user.username = email

                user.role ='user'

                password = generate_password()

                user.password = make_password(password)

                user.save()

                Wishlist.objects.create(user=user)

                Cart.objects.create(user=user)

            subject = 'Cake Tales | Login Credentials'

            recipient = email 

            template = 'emails/credentials.html'

            context = {'user':user,'password':password,'login_url':(f'{config('MY_URL')}/login/')}  

            # send_email(subject,recipient,template,context)

            thread = threading.Thread(target=send_email,args=(subject,recipient,template,context))

            thread.start()

            return redirect('login')
        
        data = {'form':form,'page':self.page}

        return render(request,self.template,context=data)
    
    