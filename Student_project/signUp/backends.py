from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import CustomUser, RecruiterProfile

class EmailOrPhoneModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            if '@' in username:
                # Check if user is a CustomUser
                user = CustomUser.objects.get(email=username)
            else:
                # Check if user is a CustomUser
                user = CustomUser.objects.get(phone=username)
        except CustomUser.DoesNotExist:
            user = None

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user

        # If not found in CustomUser, try finding in RecruiterProfile
        try:
            if '@' in username:
                recruiter_profile = RecruiterProfile.objects.get(user__email=username)
            else:
                recruiter_profile = RecruiterProfile.objects.get(user__phone=username)
        except RecruiterProfile.DoesNotExist:
            recruiter_profile = None

        if recruiter_profile and recruiter_profile.user.check_password(password) and self.user_can_authenticate(recruiter_profile.user):
            return recruiter_profile.user

        return None
