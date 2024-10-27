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


class AgronomistOrRenterPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if re.match(r'^agronom\d+$', request.user.username):
            return True
        if request.user.is_superuser:
            return True
        return request.method in ['GET', 'POST']
    def has_object_permission(self, request, view, obj):
        if re.match(r'^agronom\d+$', request.user.username):
            return True
        return obj.bed.rented_by == request.user
