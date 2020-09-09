from django import forms
from .models import ContactModel



class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-tag', 'placeholder':'Enter your Name', }))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-tag', 'placeholder':'Enter your Email Address',}))
    number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-tag', 'placeholder':'Enter your Contact No.', }))
    message = forms.CharField(widget=forms.Textarea(attrs={'class':'form-tag',' cols':'20', 'rows':'5', 'placeholder':'Enter your msg',}))

    class Meta():
        model = ContactModel
        fields = ['name', 'email', 'number', 'message']
