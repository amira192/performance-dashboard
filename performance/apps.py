from django.apps import AppConfig


class PerformanceConfig(AppConfig):
    name = 'performance'
    def ready(self):
        import performance.signals

