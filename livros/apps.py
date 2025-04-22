from django.apps import AppConfig


class LivrosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'livros'

    def ready(self):
        from .models import Usuario
        Usuario.objects.filter(is_logged=True).update(is_logged=False)