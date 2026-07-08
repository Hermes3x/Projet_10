from rest_framework import permissions


class IsSelfOrReadOnly(permissions.BasePermission):
    """Tout le monde peut lire un profil ; on ne modifie/supprime que le sien."""
    def has_object_permission(self, request, view, obj):
        # Lecture (GET…) → autorisée pour tous
        if request.method in permissions.SAFE_METHODS:
            return True

        # Écriture → seulement si l'objet EST l'utilisateur connecté
        return obj == request.user
