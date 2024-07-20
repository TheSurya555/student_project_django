# import logging
# from django import forms
# from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# from django.urls import reverse_lazy
# from django.contrib.auth.tokens import default_token_generator
# from django.core.mail import send_mail
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.template.loader import render_to_string
# from django.conf import settings
# from .forms import CustomPasswordResetForm

# logger = logging.getLogger(__name__)

# class CustomPasswordResetView(PasswordResetView):
#     form_class = CustomPasswordResetForm
#     success_url = reverse_lazy('password_reset_done')
#     template_name = 'password_reset/password_reset_form.html'
#     email_template_name = 'password_reset/password_reset_email.html'
#     subject_template_name = 'password_reset/password_reset_subject.txt'
#     token_generator = default_token_generator

#     def form_valid(self, form):
#         logger.debug("Form is valid")
#         email_or_phone = form.cleaned_data['email_or_phone']
#         logger.debug("email_or_phone: %s", email_or_phone)

#         try:
#             users = form.get_users(email_or_phone)
#             logger.debug("Users: %s", users)

#             for user in users:
#                 context = {
#                     'email': user.email,
#                     'domain': self.request.META['HTTP_HOST'],
#                     'site_name': 'Talent Sprout',
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     'user': user,
#                     'token': self.token_generator.make_token(user),
#                     'protocol': 'https' if self.request.is_secure() else 'http',
#                 }
#                 subject = render_to_string(self.subject_template_name, context).strip()
#                 email_body = render_to_string(self.email_template_name, context)
#                 subject = ' '.join(subject.split())  # Ensure no newlines or extra spaces in the subject

#                 send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
#                 logger.debug("Reset email sent to %s", user.email)
#         except forms.ValidationError as e:
#             form.add_error('email_or_phone', e)
#             logger.warning("Validation error: %s", e)
#             return self.form_invalid(form)
        
#         logger.debug("Redirecting to %s", self.success_url)
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         logger.error("Form is invalid: %s", form.errors)
#         return super().form_invalid(form)

# class CustomPasswordResetDoneView(PasswordResetDoneView):
#     template_name = 'password_reset/password_reset_done.html'

# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     success_url = reverse_lazy('password_reset_complete')
#     template_name = 'password_reset/password_reset_confirm.html'

# class CustomPasswordResetCompleteView(PasswordResetCompleteView):
#     template_name = 'password_reset/password_reset_complete.html'


import logging
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .forms import CustomPasswordResetForm

logger = logging.getLogger(__name__)

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    template_name = 'password_reset/password_reset_form.html'
    email_template_name = 'password_reset/password_reset_email.html'
    html_email_template_name = 'password_reset/password_reset_email.html'  # Add this line if you have an HTML template
    subject_template_name = 'password_reset/password_reset_subject.txt'
    token_generator = default_token_generator

    def form_valid(self, form):
        logger.debug("Form is valid")
        domain_override = self.request.META['HTTP_HOST']
        
        form.save(
            domain_override=domain_override,
            subject_template_name=self.subject_template_name,
            email_template_name=self.email_template_name,
            html_email_template_name=self.html_email_template_name,  # Pass the HTML template name here
            use_https=self.request.is_secure(),
            token_generator=self.token_generator,
            from_email=settings.DEFAULT_FROM_EMAIL,
            request=self.request
        )

        logger.debug("Redirecting to %s", self.success_url)
        return super().form_valid(form)

    def form_invalid(self, form):
        logger.error("Form is invalid: %s", form.errors)
        return super().form_invalid(form)

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'password_reset/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset/password_reset_complete.html'
