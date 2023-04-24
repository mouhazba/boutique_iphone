from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils import timezone

# Create your models here.
MODEL = (
    ('7', '7'),
    ('8', '8'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('X', 'X'),
    ('Xr', 'Xr'),
    ('Xsmax', 'Xsmax'))

CATEGORY = (
    ('Simple', 'Simple'),
    ('+', '+'),
    ('Pro', 'Pro'),
    ('Promax', 'Promax'),
)

TAILLE = (
    ('32', 32),
    ('64', 64),
    ('128', 128),
    ('256', 256),
    ('512', 512),
)


class Manager(AbstractUser):
    pass


class Iphone(models.Model):
    ime = models.CharField(max_length=120, unique=True)
    model = models.CharField(max_length=6, choices=MODEL)
    category = models.CharField(max_length=6, choices=CATEGORY)
    taille = models.CharField(max_length=3, choices=TAILLE)
    stock = models.IntegerField(default=0)
    price_acquisition = models.IntegerField(default=0)
    date_acquisition = models.DateTimeField(blank=True, null=True)
    price_marcher = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.model, self.category, self.taille}"

    def save(self, *args, **kwargs):
        if not self.date_acquisition:
            self.date_acquisition = timezone.now()

        return super().save(*args, **kwargs)


class Client(models.Model):
    iphone = models.ForeignKey(Iphone, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    nom = models.CharField(max_length=120)
    prenom = models.CharField(max_length=120)
    adresse = models.CharField(max_length=120)
    tel = models.CharField(max_length=120)
    montant = models.IntegerField(default=0)
    date_achat = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom, self.prenom}"

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)


class Moratoire(models.Model):
    iphone = models.ForeignKey(Iphone, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    nom = models.CharField(max_length=120)
    prenom = models.CharField(max_length=120)
    adresse = models.CharField(max_length=120)
    tel = models.CharField(max_length=120)
    montant = models.IntegerField(default=0)
    avance = models.IntegerField(default=0)
    restant = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom, self.prenom}"


class Versement(models.Model):
    client_moratoire = models.ForeignKey(Moratoire, on_delete=models.CASCADE)
    versement = models.IntegerField(default=0)
    restant_v = models.IntegerField(default=0)
    date_versement = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client_moratoire.nom, self.client_moratoire.prenom}"
