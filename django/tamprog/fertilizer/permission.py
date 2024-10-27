from rest_framework.permissions import BasePermission
import re

class AgronomistPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            username = request.user.username
            if re.match(r'^agronom\d+$', username):
                return True
            if request.user.is_superuser:
                return True
            return request.method in ['GET', 'HEAD', 'OPTIONS']
        return False


class BedPlantF(BasePermission):
    def has_permission(self, request, view):
        if request.user:
            username = request.user.username
            if re.match(r'^agronom\d+$', username):
                return True
            if request.user.is_superuser:
                return True
        return False
