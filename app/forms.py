from django import forms
from .models import Iphone, Client, Moratoire, Versement


class IphoneForm(forms.ModelForm):
    class Meta:
        model = Iphone
        fields = ['ime', 'model', 'category', 'taille', 'stock', 'price_acquisition', 'price_marcher']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['iphone', 'quantity', 'nom', 'prenom', 'adresse', 'tel', 'montant']


class MoratoireForm(forms.ModelForm):
    class Meta:
        model = Moratoire
        fields = ['iphone', 'quantity', 'nom', 'prenom', 'adresse', 'tel', 'montant', 'avance']


class VersementForm(forms.ModelForm):
    class Meta:
        model = Versement
        fields = ['client_moratoire', 'versement']


'''
class UserForm(forms.Form):
    msg = forms.CharField(min_length=5, required=False)
'''