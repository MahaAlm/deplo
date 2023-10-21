from django.core.management.base import BaseCommand
from django.apps import apps

class Command(BaseCommand):
    help = 'Print all models with their fields and relationships.'

    def handle(self, *args, **kwargs):
        for model in apps.get_models():
            self.stdout.write(f'\nModel: {model.__name__}')
            for field in model._meta.get_fields():
                self.stdout.write(f'    Field: {field.name} ({field.get_internal_type()})')
                if field.related_model:
                    self.stdout.write(f'        Related to: {field.related_model.__name__}')
