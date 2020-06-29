from django.apps import AppConfig


class AccountConfig(AppConfig):
    name = 'account'
    label = 'account_sacado'  # pour éviter conflit avec account de allauth
