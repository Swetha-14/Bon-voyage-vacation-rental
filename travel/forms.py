from django import forms
from .models import *
import datetime

class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['user','title','description','price','city','address','amenities','primary_image']
        widgets = {
            'user' : forms.HiddenInput(),
            'title' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title'}),
            'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Describe your place..'}),
            'price': forms.NumberInput(attrs={'class':'form-control'}),
            'city': forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
            'amenities': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Enter all the Amenities'}),
        }

class ImageForm(PlaceForm):
    image = forms.FileField(label='Other Images', widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta(PlaceForm.Meta):
        fields = PlaceForm.Meta.fields + ['image',]



