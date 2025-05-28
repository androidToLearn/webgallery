from django import forms
from .models import Image, User


class FormUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'password']


class FormImage(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
