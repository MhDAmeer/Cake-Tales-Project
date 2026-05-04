from django import forms

from .models import Profile


class LoginForm(forms.Form):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control','required': 'required'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','required': 'required'}))


    def clean(self):

        email = super().clean().get('email')

        _, domain = email.split('@')

        domain_list = ['gmail.com',
                       'yahoo.com',
                       'mailinator.com'
                       ]


        if domain not in domain_list:

            self.add_error('email', 'Invalid Email Domain')

    

        return super().clean()
    

class RegisterForm(forms.ModelForm): 


    class Meta:

        model =    Profile

        fields = ['first_name','email']

        widgets = {
                'first_name': forms.TextInput(attrs={'class': 'form-control'}),

                'email':forms.EmailInput(attrs= {'class':'form-control'}),

        }
    def clean(self):

        email = super().clean().get('email')

        _, domain = email.split('@')

        domain_list = ['gmail.com',
                       'yahoo.com',
                       'mailinator.com'
                       ]


        if domain not in domain_list:

            self.add_error('email', 'Invalid Email Domain')

        if Profile.objects.filter(username=email).exists():

            self.add_error('email','This email already taken...')

        return super().clean()