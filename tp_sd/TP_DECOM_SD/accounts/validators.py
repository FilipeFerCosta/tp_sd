from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ValidadorDeSenhaPersonalizado:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(_("A senha deve conter pelo menos um dígito."), code='senha_sem_digito')

        if not any(char.isupper() for char in password):
            raise ValidationError(_("A senha deve conter pelo menos uma letra maiúscula."), code='senha_sem_maiuscula')

        if not any(char.islower() for char in password):
            raise ValidationError(_("A senha deve conter pelo menos uma letra minúscula."), code='senha_sem_minuscula')

    def get_help_text(self):
        return _(
            "Sua senha deve conter pelo menos um dígito, uma letra maiúscula e uma letra minúscula."
        )
