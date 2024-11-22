from rest_framework.permissions import BasePermission
import re
from logging import getLogger

log = getLogger(__name__)

class PostOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            log.debug("User is allowed to POST")
            return True
        log.debug("User is not allowed to POST")
        return request.user and request.user.is_authenticated

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

class NoPostAllowed(BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            log.debug("User is not allowed to POST")
            return False
        log.debug("User is allowed to POST")
        return True