from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    """
    On ajoute une permission pour que l'utilisateur n'accéde qu'a ses propres données.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:  # Si l'utilisateur est admin
            return True
        return obj.user == request.user