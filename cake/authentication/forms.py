from django import forms

from .models import Profile


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','required':'required'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','required':'required'}))

    def clean(self):

        email = super().clean().get('email')

        _,domain = email.split('@')

        domain_list = [
                        'gmail.com',
                        'yahoo.com',
                        'mailinator.com'

                      ]
        
        if domain not in domain_list :

            self.add_error('email','invalid email domain')

        return super().clean()
    
class RegisterForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = ['first_name','email']

        widgets = {

            'first_name':forms.TextInput(attrs={'class':'form-control'}),

            'email' : forms.EmailInput(attrs={'class':'form-control'})
        }

    def clean(self):

        email = super().clean().get('email')

        _,domain = email.split('@')

        domain_list = [
                        'gmail.com',
                        'yahoo.com',
                        'mailinator.com'
                      ]
        
        if domain not in domain_list :

            self.add_error('email','invalid email domain')

        if Profile.objects.filter(username=email).exists():

            self.add_error('email','this email already taken')

        return super().clean()

class OTPForm(forms.Form):

    otp = forms.CharField(max_length=4,widget=forms.TextInput(attrs={'class':'form-control','required':'required','placeholder':'Enter OTP'}))

    def clean(self):

        otp = super().clean().get('otp')

        if len(otp)<4 :

            self.add_error('otp','input 4 digit OTP')

        return super().clean()
    
class PasswordForm(forms.Form):

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','required':'required'}))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','required':'required'}))

    def clean(self):

        password = super().clean().get('password')

        confirm_password = super().clean().get('confirm_password')
        
        if password != confirm_password:

            self.add_error('confirm_password','Password Mismatch')

        return super().clean()
    
class ForgotPasswordForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','required':'required'}))

    def clean(self):

        email = super().clean().get('email')

        _,domain = email.split('@')

        domain_list = [
                        'gmail.com',
                        'yahoo.com',
                        'mailinator.com'

                      ]
        
        if domain not in domain_list :

            self.add_error('email','invalid email domain')

        if not Profile.objects.filter(username=email).exists():

            self.add_error('email','not a registered email')

        return super().clean()
    