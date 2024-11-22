from rest_framework.permissions import BasePermission
import re
from logging import getLogger

log = getLogger(__name__)

class AgronomistPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            username = request.user.username
            if re.match(r'^agronom\d+$', username):
                log.debug(f"User {username} is an agronomist")
                return True
            if request.user.is_superuser:
                log.debug(f"User {username} is a superuser")
                return True
            log.debug(f"User {username} is not an agronomist")
            return request.method in ['GET', 'HEAD', 'OPTIONS']
        log.debug("User is not authenticated")
        return False


class AgronomistOrRenterPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            log.debug("User is not authenticated")
            return False
        if re.match(r'^agronom\d+$', request.user.username):
            log.debug(f"User {request.user.username} is an agronomist")
            return True
        if request.user.is_superuser:
            log.debug(f"User {request.user.username} is a superuser")
            return True
        log.debug(f"User {request.user.username} is not an agronomist")
        return request.method in ['GET', 'POST']
    def has_object_permission(self, request, view, obj):
        if re.match(r'^agronom\d+$', request.user.username):
            log.debug(f"User {request.user.username} is an agronomist")
            return True
        log.debug(f"User {request.user.username} is not an agronomist")
        return obj.bed.rented_by == request.user
