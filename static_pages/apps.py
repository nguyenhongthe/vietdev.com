from django.apps import AppConfig


class StaticPagesConfig(AppConfig):
    name = 'static_pages'

    def ready(self):
        import static_pages.signals