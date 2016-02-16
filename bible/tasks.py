from __future__ import absolute_import
from celery import shared_task, group, chord, subtask
from . import importer, models
import itertools
import requests


def import_full():
    # Import all enabled translations in all enabled languages, forming the intersection of an edition
    langs = models.Language.objects.all()
    imp_eds = group(import_editions.s(l.iso_2_code) for l in langs)()
    eids = list(itertools.chain(*imp_eds.get()))

    # Import book and chapter objects for every imported edition
    cids = group(import_books.s(eid) for eid in eids)()
    cids = list(itertools.chain(*cids.get()))

    # Import verse and footnote content for every chapter
    imp_chap = group(import_chapter.s(cid) for cid in cids)()
    imp_chap.get()

    # Index the footnotes and marginal references
    idx_notes = group(index_refs.s(cid) for cid in cids)()
    idx_notes.get()


@shared_task(bind=True, throws=(importer.ImporterError, requests.RequestException))
def import_editions(self, iso_2_code):
    language = models.Language.objects.get(iso_2_code=iso_2_code)
    try:
        editions = importer.import_editions(language)
    except (importer.ImporterError, requests.RequestException) as e:
        self.retry(exc=e)
    return [e.id for e in editions]


@shared_task(bind=True, throws=(importer.ImporterError, requests.RequestException))
def import_books(self, edition_id):
    edition = models.Edition.objects.get(pk=edition_id)
    try:
        books = importer.import_books(edition)
    except (importer.ImporterError, requests.RequestException) as e:
        self.retry(exc=e)

    cids = []
    for book in books:
        try:
            chapters = importer.import_chapters(book)
        except (importer.ImporterError, requests.RequestException) as e:
            self.retry(exc=e)
        cids += [c.id for c in chapters]
    return cids


@shared_task(bind=True, throws=(importer.ImporterError, requests.RequestException))
def import_chapter(self, chapter_id):
    chapter = models.Chapter.objects.get(pk=chapter_id)
    try:
        importer.import_chapter(chapter)
    except (importer.ImporterError, requests.RequestException) as e:
        self.retry(exc=e)
    return True


@shared_task(bind=True, throws=(importer.ImporterError, ))
def index_refs(self, chapter_id):
    chapter = models.Chapter.objects.get(pk=chapter_id)
    importer.index_refs(chapter)
    return True
