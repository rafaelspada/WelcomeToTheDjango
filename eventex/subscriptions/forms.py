from django import forms


class SubscriptionForm(forms.Form):
    name = forms.CharField(label='Name')
    cpf = forms.CharField(label='CPF')
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Telefone')