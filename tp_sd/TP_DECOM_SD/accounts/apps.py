from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TP_DECOM_SD.accounts'

    def ready(self):
        import TP_DECOM_SD.accounts.signals  # Importa os sinais
