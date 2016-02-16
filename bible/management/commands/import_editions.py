from bible import tasks, models
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import edition data for all languages'

    def handle(self, *args, **options):
        tasks.import_full()
