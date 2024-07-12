import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            raise ValidationError(
                _("Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."),
                code='invalid_password',
            )

    def get_help_text(self):
        return _(
            "Your password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, one digit, and one special character."
        )
