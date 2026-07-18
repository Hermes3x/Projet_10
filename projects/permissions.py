from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """L'auteur peut tout faire ; les autres, lecture seule."""

    def has_object_permission(self, request, view, obj):
        # Si c'est une méthode de lecture (GET, HEAD, OPTIONS) → autorisé pour tous
        if request.method in permissions.SAFE_METHODS:
            return True

        # Sinon (PUT, PATCH, DELETE) → autorisé seulement si l'utilisateur est l'auteur
        return obj.author == request.user


class IsProjectAuthorOrReadOnly(permissions.BasePermission):
    """Seul l'auteur du projet peut modifier/supprimer ; les autres, lecture seule."""

    def has_object_permission(self, request, view, obj):
        """Lecture (GET, HEAD, OPTIONS) → autorisée pour tout contributeur""" 
        if request.method in permissions.SAFE_METHODS:
            return True

        """Écriture (DELETE, PATCH…) → seulement l'auteur du projet lié"""
        return obj.project.author == request.user
