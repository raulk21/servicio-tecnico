from django import forms
from .models import ContactRequest

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone', 'email', 'message', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class RepairRequestForm(forms.ModelForm):

    class Meta:
        model = ContactRequest
        fields = ['name','email','phone','service','message']

        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control mb-4'}),
            'email': forms.EmailInput(attrs={'class':'form-control mb-4'}),
            'phone': forms.TextInput(attrs={'class':'form-control mb-4'}),
            'service': forms.Select(attrs={'class':'form-control mb-4'}),
            'message': forms.Textarea(attrs={'class':'form-control','rows':8}),
        }