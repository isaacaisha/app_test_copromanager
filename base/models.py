# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('superadmin', 'Super Administrateur'),
        ('syndic', 'Syndic'),
        ('coproprietaire', 'Copropriétaire'),
        ('prestataire', 'Prestataire'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='coproprietaire')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class Licence(models.Model):
    syndic = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'syndic'})
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=[('active', 'Active'), ('expiree', 'Expirée')])
    options_specifiques = models.TextField(blank=True, null=True)
    version_dossier = models.CharField(max_length=10, default='v1')  # Tracking version

    def __str__(self):
        return f"Licence de {self.syndic.username} - Statut: {self.statut}"


class Document(models.Model):
    TYPES_DOCUMENTS = [
        ('assurance', 'Assurance'),
        ('devis', 'Devis'),
        ('facture', 'Facture'),
    ]
    auteur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type_document = models.CharField(max_length=20, choices=TYPES_DOCUMENTS)
    fichier = models.FileField(upload_to='documents/')
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_document} ajouté par {self.auteur.username}"
