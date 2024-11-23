from rest_framework.permissions import BasePermission
import re
from logging import getLogger

log = getLogger(__name__)

class AgronomistPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            username = request.user.username
            if re.match(r'^agronom\d+$', username):
                log.debug(f'User {username} has permission to access the view')
                return True
            if request.user.is_superuser:
                log.debug(f'User {username} is a superuser and has permission to access the view')
                return True
            log.debug(f'User {username} does not have permission to access the view')
            return request.method in ['GET', 'HEAD', 'OPTIONS']
        log.debug('Anonymous user does not have permission to access the view')
        return False

