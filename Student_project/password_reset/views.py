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
