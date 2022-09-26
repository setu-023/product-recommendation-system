import requests
from rest_framework.permissions import BasePermission


class CustomePermission(BasePermission):

    def has_permission(self, request, view):
        print( request.user.user_type )
        if request.user.user_type == 'admin' or request.user.user_type == 'vendor':
                return True
        else:
            return False    