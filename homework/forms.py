from django import forms


class UserForm(forms.Form):
    name= forms.CharField(max_length=100)
    surname= forms.CharField(max_length=100)
    full_name = forms.CharField(max_length=100)