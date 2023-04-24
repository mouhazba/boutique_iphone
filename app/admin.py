from django.contrib import admin
from .models import Iphone, Client, Moratoire, Versement, Manager


# Register your models here.
@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    model = Manager
    list_display = ['username']


@admin.register(Iphone)
class IphoneAdmin(admin.ModelAdmin):
    model = Iphone
    list_display = ['id', 'ime', 'model', 'category', 'taille', 'stock', 'price_acquisition', 'price_marcher',
                    'date_acquisition']


@admin.register(Client)
class ClientsAdmin(admin.ModelAdmin):
    model = Client
    list_display = ['nom', 'prenom', 'adresse', 'tel', 'iphone', 'quantity', 'montant', 'date_achat']


@admin.register(Moratoire)
class MoratoireAdmin(admin.ModelAdmin):
    model = Moratoire
    list_display = ['nom', 'prenom', 'adresse', 'tel', 'iphone', 'quantity', 'montant', 'avance', 'restant', 'date']


@admin.register(Versement)
class VersementAdmin(admin.ModelAdmin):
    model = Versement
    list_display = ['client_moratoire', 'versement', 'date_versement']

