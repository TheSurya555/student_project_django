import logging
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

User = get_user_model()

logger = logging.getLogger(__name__)

class CustomPasswordResetForm(forms.Form):
    email_or_phone = forms.CharField(max_length=254, required=True, widget=forms.TextInput(attrs={'class': 'input', 'autocomplete': 'off'}))

    def clean_email_or_phone(self):
        email_or_phone = self.cleaned_data['email_or_phone']
        logger.debug(f"clean_email_or_phone: {email_or_phone}")
        # Validate if the user exists by email or phone
        if not User.objects.filter(email=email_or_phone).exists() and not User.objects.filter(phone=email_or_phone).exists():
            raise ValidationError("No user is associated with this email or phone number.")
        return email_or_phone

    def get_users(self, email_or_phone):
        # Return queryset of users matching email or phone
        users = User.objects.filter(email=email_or_phone) | User.objects.filter(phone=email_or_phone)
        logger.debug(f"get_users: {users}")
        return users

    def save(self, domain_override=None,
             subject_template_name=None,
             email_template_name=None,
             html_email_template_name=None,
             use_https=False,
             token_generator=None,
             from_email=None,
             request=None,
             **kwargs):

        email_or_phone = self.cleaned_data['email_or_phone']
        users = self.get_users(email_or_phone)
        for user in users:
            context = {
                'email': user.email,
                'domain': domain_override,
                'site_name': 'Talent Sprout',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': 'https' if use_https else 'http',
            }
            subject = render_to_string(subject_template_name, context).strip()
            email_body = render_to_string(email_template_name, context)
            subject = ' '.join(subject.split())  # Ensure no newlines or extra spaces in the subject

            if html_email_template_name:
                html_email_body = render_to_string(html_email_template_name, context)
            else:
                html_email_body = None

            send_mail(subject, email_body, from_email, [user.email], fail_silently=False, html_message=html_email_body)
            logger.debug("Reset email sent to %s", user.email)
