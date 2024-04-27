from django.apps import AppConfig
from django.apps import AppConfig
from django.core.mail import send_mail
from django.template.loader import render_to_string

class SlmsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'slmsapp'

    def ready(self):
        import slmsapp.signals