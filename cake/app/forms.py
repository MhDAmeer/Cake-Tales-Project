from django import forms

from .models import Cake


class CakeForm(forms.ModelForm):

    class Meta:

        model = Cake

        # fields = ['name','des']

        #fields = '__all__'

        exclude = ['active_status','uuid']

        widgets = {

            'name':forms.TextInput(attrs={'class':'form-control'}),
            
            'description':forms.Textarea(attrs={'class':'form-control'}),
            
            'photo':forms.FileInput(attrs={'class':'form-control'}),
            
            'category':forms.Select(attrs={'class':'form-select'}),
            
            'flavour':forms.Select(attrs={'class':'form-select'}),
            
            'weight':forms.Select(attrs={'class':'form-select'}),
            
            'shape':forms.Select(attrs={'class':'form-select'}),
            
            'egg_added':forms.RadioSelect(attrs={'class':'form-check-input border border-3'}, choices = [(True,'Yes'),(False,'No')]),  

            'is_available':forms.RadioSelect(attrs={'class':'form-check-input border border-3'}, choices = [(True,'Available'),(False,'Not Available')]),

            'price':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter price '}),

        }