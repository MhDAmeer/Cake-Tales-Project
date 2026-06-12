from django import forms

from .models import Cake,DeliveryAddress

class CakeForm(forms.ModelForm):

    class Meta:

        model = Cake

        # fields = ['name','description']

        # fields = '__all__'

        exclude = ['active_status','uuid']

        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),

            'description':forms.Textarea(attrs={'class':'form-control','rows':3}),

            'photo':forms.FileInput(attrs={'class':'form-control'}),

            'category':forms.Select(attrs={'class':'form-select'}),

            'flavour':forms.Select(attrs={'class':'form-select'}),

            'weight':forms.Select(attrs={'class':'form-select'}),

            'shape':forms.Select(attrs={'class':'form-select'}),

            'egg_added':forms.RadioSelect(attrs={'class':'form-check-input border border-3'},choices=[(True,'Yes'),(False,'No')]),

            'is_available':forms.RadioSelect(attrs={'class':'form-check-input border border-3'},choices=[(True,'Available'),(False,'Not Available')]),

            'price':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter price in ₹'}),


        }

class DeliveryAddressForm(forms.ModelForm):

    class Meta:

        model = DeliveryAddress

        fields = [
            'house_num_or_building_name',
            'landmark',
            'place',
            'pincode',
        ]

        widgets = {

            'house_num_or_building_name': forms.TextInput(attrs={'class':'form-control'}),

            'landmark': forms.Textarea(attrs={'class':'form-control'}),

            'place': forms.TextInput(attrs={'class':'form-control'}),

            'pincode': forms.TextInput(attrs={'class':'form-control'}),
        }

        