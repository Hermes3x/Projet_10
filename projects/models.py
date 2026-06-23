from django.db import models
from django.conf import settings
import uuid


class Project(models.Model):

    # Détails du projets
    name = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    # Type
    TYPE_CHOICES = [
        ('back-end', 'Back-end'),
        ('front-end', 'Front-end'),
        ('iOS', 'iOS'),
        ('Android', 'Android'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    # L'auteur du projet
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_projects')

    # Horodatage de la ressource
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contributor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='contributions'
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='contributors'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'project'],

                name='unique_contributor_per_project'
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.project}"



class Issue(models.Model):
    # Nom du problème
    name = models.CharField(max_length=255)

    # Description du problème
    description = models.TextField(blank=True)

    # L'utilisateur auquel le problèle est assign
    # Je ne connais pas bien le fonctionnement de ce genre de projet = 
    # Un utilisateur crée un probleme qui le concerne ? dans ce cas foreykey -> user loggé
    # Ou un utilisateur crée un problème pour un autre utilisateur (qui ne se log pas forcément sur l'application)?
    # Je déduis la 2eme solution car sinon author = utilisateur
    assignation = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # SET_NULL = si l'utilisateur est supprimé l'issue ne disaprait pas
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_issues'
    )

    # Priorité
    PRIORITY_CHOICES = [
        ('low', 'LOW'),
        ('medium', 'MEDIUM'),
        ('high', 'HIGH'),
    ]

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)

    # Tag
    TAG_CHOICES = [
        ('bug', 'BUG'),
        ('feature', 'FEATURE'),
        ('task', 'TASK'),
    ]

    tag = models.CharField(max_length=20, choices=TAG_CHOICES)

    # Status
    STATUS_CHOICES = [
        ('to_do', 'To DO'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='to_do')

    # Affiliation au projet
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='issues'
    )

    # L'auteur du probleme
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # SET_NULL = issue conservé même si auteur est supprimé
        on_delete=models.SET_NULL,
        null=True,
        related_name='authored_issues'
    )

    # Horodatage de la ressource
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.project.name}"


class Comment(models.Model):
    # Corps du commentaire
    description = models.TextField()

    # Unique ID
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Affiliation au problème
    issue = models.ForeignKey(
        Issue,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    # Affiliation à l'auteur
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_comments'
    )

    # Horodatage de la ressource
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.uuid} - {self.issue.name}"
