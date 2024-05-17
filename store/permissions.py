from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request:Request, view):
        if request.method in SAFE_METHODS:
            return True 
        
        return bool(request.user and request.user.is_staff)


class HasPermissionHitory(permissions.BasePermission):
    """
    Allows access only to the user with this permissions
    """
    def has_permission(self, request:Request, view):
        print("Permission Checker:")
        return request.user.has_perm('store.view_history')


class DjanggoObjectsPermisions(permissions.DjangoObjectPermissions):
     
     def __init__(self) -> None:
         self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
