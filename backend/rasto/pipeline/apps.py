from django.apps import AppConfig


class Config(AppConfig):
    name = "rasto.pipeline"
    label = "pipeline"
    default_auto_field = "django.db.models.BigAutoField"
