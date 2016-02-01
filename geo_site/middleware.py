from django.conf import settings
from django.views.debug import technical_500_response
import sys

EX_GROUP_NAME = getattr(settings, 'TECHNICAL_500_GROUP_NAME', 'Technical Errors')

class UserBasedExceptionMiddleware(object):
    def process_exception(self, request, exception):
        exc_info = sys.exc_info()
        user = request.user
        if not user.is_superuser:
            return None
        if user.groups.filter(name=EX_GROUP_NAME):
            return technical_500_response(request, *exc_info)
        return None