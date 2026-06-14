from django.db import models
from django.conf import settings


class Project(models.Model):
    # Type
    TYPE_CHOICES = [
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]

    # Détails du projets
    # Horodatage de la ressource
    date_created = models.DateTimeField(auto_now_add=True)
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # L'auteur du projet
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_projects')

    def __str__(self):
        return self.name

class Issues(models.Model):
    pass


class Comments(models.Model):
    pass
