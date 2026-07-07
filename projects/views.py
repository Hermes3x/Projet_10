from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly, IsProjectAuthorOrReadOnly
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Project, Contributor, Issue, Comment
from .serializers import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        return Project.objects.filter(contributors__user=self.request.user)

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user=self.request.user, project=project)


class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated, IsProjectAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Contributor.objects.filter(project__contributors__user=self.request.user)
        project_id = self.request.GET.get('project_id')
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)

        return queryset

    def perform_create(self, serializer):
        project = serializer.validated_data.get('project')

        if project.author != self.request.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à accéder à ce contenu")

        serializer.save()


class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def get_queryset(self):
        # Récupérer toutes les issues d'un projet dont l'utilisateur connecté est contributeur
        queryset = Issue.objects.filter(project__contributors__user=self.request.user)

        # Filterer les issues par projet
        project_id = self.request.GET.get('project_id')

        # Si une ID de projet existe alors retourne les issues de cette ID
        if project_id is not None:
            queryset = queryset.filter(project_id=project_id)

        # Retourne les issues du projets 
        return queryset

    def perform_create(self, serializer):
        # Récupérer le projet envoyé dans la requête
        project = serializer.validated_data.get('project')

        # Vérifier si l'utilisateur est un contributeur du projet
        is_contributor = Contributor.objects.filter(
            user=self.request.user,
            project=project
        ).exists()

        # Bloquer utilisateur si pas contributeur
        if not is_contributor:
            raise PermissionDenied("Vous n'êtes pas autorisé à accéder à ce contenu")

        # Si c'est bon, on sauvegarde l'issue et auteur = utilisateur connecté
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    # On appel le serializer de comment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    # On récupère les comments d'un projet dont l'utilisateur est contributeur dans la requête 
    def get_queryset(self):
        queryset = Comment.objects.filter(issue__project__contributors__user=self.request.user)
        issue_id = self.request.GET.get('issue_id')
        if issue_id is not None:
            queryset = queryset.filter(issue_id=issue_id)

        return queryset

    def perform_create(self, serializer):
        # Récupérer l'issue envoyée dans la requete
        issue = serializer.validated_data.get('issue')

        # Récupérer le projet relatif à l'issue
        project = issue.project

        # Vérifier si l'utilisateur est un contributeur du projet
        is_contributor = Contributor.objects.filter(
            user=self.request.user,
            project=project,
        ).exists()

        # Bloquer utilisateur si pas contributeur
        if not is_contributor:
            raise PermissionDenied("Vous n'êtes pas autorisé à accéder à ce contenu")

        serializer.save(author=self.request.user)
