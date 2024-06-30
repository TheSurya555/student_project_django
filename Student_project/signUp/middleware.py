# In signUp/middleware.py

from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from datetime import timedelta

class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            request.user.update_last_activity()
        return None
