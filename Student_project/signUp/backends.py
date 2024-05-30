from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import RequiterUser

class EmailOrPhoneModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(phone=username)
        except User.DoesNotExist:
            user = None

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

        # Try authentication using RequiterUser model
        try:
            if '@' in username:
                requiter_user = RequiterUser.objects.get(email=username)
            else:
                requiter_user = RequiterUser.objects.get(phone=username)
        except RequiterUser.DoesNotExist:
            requiter_user = None

        if requiter_user and requiter_user.check_password(password) and self.user_can_authenticate(requiter_user):
            return requiter_user

        return None
