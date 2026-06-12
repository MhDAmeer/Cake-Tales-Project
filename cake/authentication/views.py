from django.shortcuts import render,redirect

# Create your views here.
from django.views import View

from . forms import LoginForm,RegisterForm,OTPForm,PasswordForm,ForgotPasswordForm

from django.contrib.auth import authenticate,login,logout

from cake.utility import generate_password,send_email,generate_otp

from django.contrib.auth.hashers import make_password

from decouple import config

import threading

from app.models import Wishlist,Cart

from django.db import transaction

from django.contrib import messages

from .models import OTP,Profile

from django.utils import timezone

from django.contrib.auth.hashers import make_password

class Loginview(View):

    template = 'authentication/login.html'

    form_class = LoginForm

    page = 'Login'


    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        error = None

        if form.is_valid():

            email = form.cleaned_data.get('email')

            password = form.cleaned_data.get('password')

            user = authenticate(username=email,password=password)

            error = 'invalid credentials '

            if user :

                login(request,user)

                messages.success(request,'Successfully Logined')

                return redirect('home')
            
            error = 'invaild credentials '
            
            

        data = {'form': form,'page':self.page,'error':error}

        return render(request,self.template,context=data)
    
class LogoutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)

        return redirect('home')

class RegisterView(View):

    template = 'authentication/register.html'

    form_class = RegisterForm

    page = 'Signup'

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'form':form,'page':self.page}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            with transaction.atomic():

              user = form.save(commit=False)

              email = form.cleaned_data.get('email')

              user.username = email

              user.role = 'User'

              password = generate_password()

            # print(password)

              user.password = make_password(password)

              user.save()

              Wishlist.objects.create(user=user)

              Cart.objects.create(user=user)

            subject = 'Cake Tales | Login Credentials'

            recipient = email

            template = 'emails/credentials.html'

            context = {'user':user,'password':password,'login_url':(f'{config('MY_URL')}/login/')}

            # send_email(subject,recipient,template,context)

            thread = threading.Thread(target=send_email,args=[subject,recipient,template,context])

            thread.start()

            return redirect('login')
        
        data = {'form':form,'page':self.page}

        return render(request,self.template,context=data)

class GenerateOTPView(View):

    template = 'authentication/otp.html'

    page = 'Generate Otp'

    form_class = OTPForm

    def get(self,request,*args,**kwargs):

        if request.user and request.user.is_authenticated :

            user =request.user

        else:

            email = request.session.get('email')

            user = Profile.objects.get(username=email)

        otp = generate_otp()

        otp_obj,_= OTP.objects.get_or_create(user=user)

        otp_obj.otp = otp

        otp_obj.save()

        subject = 'Cake Tales | Change Password'

        recipient = user.email

        template = 'emails/email-otp.html'

        context = {'user':user,'otp':otp}

        thread = threading.Thread(target=send_email,args=[subject,recipient,template,context])

        thread.start()

        form = self.form_class()

        remaining_time = 300

        request.session['otp_time'] = timezone.now().timestamp()

        data = {'page':self.page, 'form':form,'remaining_time':remaining_time}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwagrs):

        form = self.form_class(request.POST)

        if form.is_valid():

            if request.user and request.user.is_authenticated :

                user =request.user

            else:

                email = request.session.get('email')

                user = Profile.objects.get(username=email)

            user_otp = form.cleaned_data.get('otp')

            db_otp = user.otp.otp

            otp_time = request.session['otp_time']

            msg = None

            if otp_time:

                elapsed_time = timezone.now().timestamp()-otp_time

                if elapsed_time > 300:

                    msg = 'OTP Expired'

                elif user_otp == db_otp:

                    user.otp.otp_verified = True

                    user.otp.save()
                    
                    messages.success(request,'OTP Successfully Verifed')

                    return redirect('set-password')
                
                else:

                    msg = 'Invaild OTP'

        remaining_time = max(0,300-elapsed_time)

        data = {'form':form,'msg':msg,'remaining_time':remaining_time}

        return render(request,self.template,context=data)

class SetPasswordView(View):

    template = 'authentication/set-password.html'

    page = 'Set Password'

    form_class = PasswordForm

    def get(self,request,*args,**kwargs):

        if request.user and request.user.is_authenticated :

            user =request.user

        else:

            email = request.session.get('email')

            user = Profile.objects.get(username=email)

        if user.otp.otp_verified:

            form = self.form_class()

            data = {'page':self.page, 'form':form}

            return render(request,self.template,context=data)
        
        return redirect('generate-otp')
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            if request.user and request.user.is_authenticated :

                user =request.user

            else:

                email = request.session.get('email')

                user = Profile.objects.get(username=email)

            password = form.cleaned_data.get('password')

            user.password = make_password(password)

            user.save()

            user.otp.otp_verified = False

            user.otp.save()

            request.session.clear()

            logout(request)

            messages.success(request,'Password Updated Successfully')

            return redirect('login')

class ForgotPassword(View):

    template = 'authentication/forgot-password.html'

    page = 'Forgot Password'

    form_class = ForgotPasswordForm

    def get(self,request,*args,**kwargs):

        form = self.form_class()

        data = {'page':self.page, 'form':form}

        return render(request,self.template,context=data)
    
    def post(self,request,*args,**kwargs):

        form = self.form_class(request.POST)

        if form.is_valid():

            email = form.cleaned_data.get('email')

            request.session['email'] = email

            return redirect('generate-otp')
        
        data = {'form': form}
        
        return render(request,self.template,context=data)
    
