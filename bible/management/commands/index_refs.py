from bible import importer, models
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import edition data for all languages'

    def handle(self, *args, **options):
        for chapter in models.Chapter.objects.all():
            importer.index_refs(chapter)
