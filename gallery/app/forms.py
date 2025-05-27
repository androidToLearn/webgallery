<<<<<<< HEAD
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
=======
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
>>>>>>> 494cc95ff01940e6a9be0350084b1fd140572d7d
