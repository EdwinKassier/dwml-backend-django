"""Domain app configuration."""

from django.apps import AppConfig


class DomainConfig(AppConfig):
    """Configuration for the domain app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "domain"
    verbose_name = "DWML Domain"
