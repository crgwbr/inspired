import requests
import logging
import simplejson
import re
from bs4 import BeautifulSoup
from celery import chord
from django.db import transaction
from . import models


logger = logging.getLogger(__name__)


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}


class ImporterError(Exception):
    pass


def import_editions(language):
    logger.info('Importing editions for Language[%s]' % language)

    resp = requests.get(language.edition_api, headers=HEADERS)
    editions_data = resp.json().get('langs', {}).get(language.iso_2_code, {}).get('editions')
    if not editions_data:
        raise ImporterError('No edition data found for Language[%s]' % language)

    for edition_data in editions_data:
        try:
            translation = models.Translation.objects.get(symbol=edition_data['symbol'])
        except models.Translation.DoesNotExist:
            logger.info('Skipping %s' % edition_data['symbol'])
            continue

        with transaction.atomic():
            try:
                edition = models.Edition.objects.get(language=language, translation=translation)
            except models.Edition.DoesNotExist:
                edition = models.Edition(language=language, translation=translation)
            edition.title = edition_data['title']
            edition.content_api = edition_data['contentAPI']
            edition.save()

        logger.info('Saved Edition: %s' % edition)
        yield edition


def import_books(edition):
    logger.info('Importing books for Edition[%s]' % edition)
    resp = requests.get(edition.content_api, headers=HEADERS)
    books_data = resp.json().get('editionData', {}).get('books')
    if not books_data:
        raise ImporterError('No book data found for Edition[%s]' % edition)

    for book_num, book_data in books_data.items():
        with transaction.atomic():
            try:
                book = models.Book.objects.get(edition=edition, book_num=book_num)
            except models.Book.DoesNotExist:
                book = models.Book(edition=edition, book_num=book_num)
            book.chapter_count = int(book_data['chapterCount'])
            book.has_audio = book_data['hasAudio']
            book.standard_name = book_data['standardName']
            book.standard_abbr = book_data['standardAbbreviation']
            book.official_abbr = book_data['officialAbbreviation']
            book.standard_singular_name = book_data['standardSingularBookName']
            book.standard_singular_abbr = book_data['standardSingularAbbreviation']
            book.official_singular_abbr = book_data['officialSingularAbbreviation']
            book.standard_plural_name = book_data['standardPluralBookName']
            book.standard_plural_abbr = book_data['standardPluralAbbreviation']
            book.official_plural_abbr = book_data['officialPluralAbbreviation']
            book.url_segment = book_data['urlSegment']
            book.save()
        logger.info('Saved Book: %s' % book)
        yield book


def import_chapters(book):
    logger.info('Importing chapters for %s' % book)
    for chapter_num in range(1, book.chapter_count + 1):
        chapter, created = models.Chapter.objects.get_or_create(book=book, chapter_num=chapter_num)
        yield chapter


def import_chapter(chapter):
    start_id = models.Verse.build_id(chapter.book.book_num, chapter.chapter_num, 1)
    end_id = models.Verse.build_id(chapter.book.book_num, chapter.chapter_num, 999)

    url = "%shtml/%s-%s" % (chapter.book.edition.content_api, start_id, end_id)
    resp = requests.get(url, timeout=5, headers=HEADERS)

    ranges = resp.json().get('ranges', {})

    for vsid, vsrange in ranges.items():
        logger.info('Importing verses %s' % vsid)
        with transaction.atomic():
            import_verses(chapter, vsrange['html'])
            import_footnotes(chapter.book.edition, vsrange['footnotes'])


def index_refs(chapter):
    logger.info('Indexing references in %s' % chapter)
    for verse in models.Verse.objects.filter(chapter=chapter):
        soup = BeautifulSoup(verse.content, 'html.parser')
        with transaction.atomic():
            update_footnote_refs(chapter.book.edition, verse, soup)
            update_xrefs(chapter.book.edition, verse, soup)
            verse.content = str(soup)
            verse.save()


def update_footnote_refs(edition, verse, soup):
    notes = []
    for link in soup.find_all('a', class_=re.compile("^(footnoteLink|footnote)$")):
        fnid = link['href'].lstrip('#')
        try:
            note = models.Footnote.objects.get(edition=edition, fnid=fnid)
            notes.append(note)
        except models.Footnote.DoesNotExist:
            logger.error('Could not link missing Footnote[%s]', fnid)
        link['class'] = 'footnote'
        del link['id']
    verse.footnotes = notes


def update_xrefs(edition, verse, soup):
    ref_type = models.VerseRelationshipType.objects.get(code=models.VerseRelationshipType.T_XREF)

    refs = []
    for link in soup.find_all('a', class_=re.compile("^(xrefLink|marginal-ref)")):
        verse_refs = []
        targets = models.Verse.parse_range( link.attrs.get('data-targetverses') )
        for target in targets:
            try:
                target_verse = models.Verse.find_by_id(edition, target)
                verse_refs.append(target_verse)
                refs.append(target_verse)
            except models.Verse.DoesNotExist:
                logger.error('Could not link missing Verse[%s]', target)

        targets = simplejson.loads( link.attrs.get('data-verses', '[]') )
        for target in targets:
            try:
                target_verse = models.Verse.objects.get(id=target)
                verse_refs.append(target_verse)
                refs.append(target_verse)
            except models.Verse.DoesNotExist:
                logger.error('Could not link missing Verse[%s]', target)

        link['class'] = 'marginal-ref'
        link['href'] = '#xrefs%s' % verse.id
        link['data-verses'] = simplejson.dumps([v.id for v in verse_refs])
        del link['data-targetverses']
        del link['id']

    ref_ids = [v.id for v in refs]
    models.VerseRelationship.objects\
        .filter(from_verse=verse)\
        .exclude(to_verse__in=ref_ids)\
        .filter(relationship_type=ref_type)\
        .all().delete()

    for ref in refs:
        models.VerseRelationship.objects.get_or_create(
            relationship_type=ref_type,
            from_verse=verse,
            to_verse=ref)


def import_verses(chapter, html):
    soup = BeautifulSoup(html, 'html.parser')

    for v in soup.find_all("span", class_="verse"):
        vsid = models.Verse.parse_id(v['id'])

        # Clean up links
        for link in v.find_all("a"):
            clean_links(link)

        # Save verse object
        try:
            verse = models.Verse.objects.get(chapter=chapter, verse_num=vsid.verse_num)
        except models.Verse.DoesNotExist:
            verse = models.Verse(chapter=chapter, verse_num=vsid.verse_num)
        verse.content = str(v)
        verse.save()


def import_footnotes(edition, html):
    soup = BeautifulSoup(html, 'html.parser')

    for f in soup.find_all("div", class_="footnote"):

        # Clean up links
        for link in f.find_all("a"):
            clean_links(link)

        # Save Footnote object
        try:
            note = models.Footnote.objects.get(edition=edition, fnid=f['id'])
        except models.Footnote.DoesNotExist:
            note = models.Footnote(edition=edition, fnid=f['id'])
        note.content = str(f)
        note.save()


def clean_links(link):
    href = link.attrs.get('href', '')
    href = href.split('#').pop() if '#' in href else None
    if href:
        link['href'] = '#%s' % href
    else:
        del link['href']

    del link['data-anchor']
    del link['data-audioverses']
    del link['data-bible']
