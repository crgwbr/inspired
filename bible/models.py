from bs4 import BeautifulSoup
from django.db import models
from collections import namedtuple


VerseID = namedtuple('VerseID', ('book_num', 'chapter_num', 'verse_num'))


class Language(models.Model):
    iso_2_code = models.CharField(max_length=2, unique=True)
    wt_code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)
    edition_api = models.URLField(max_length=200)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.name


class Translation(models.Model):
    symbol = models.CharField(max_length=10, unique=True)

    class Meta:
        ordering = ('id', )

    def __str__(self):
        return self.symbol


class Edition(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='editions')
    translation = models.ForeignKey(Translation, on_delete=models.CASCADE, related_name='editions')
    title = models.CharField(max_length=150)
    content_api = models.URLField(max_length=200)

    class Meta:
        ordering = ('id', )
        unique_together = (
            ("language", "translation"),
        )

    def __str__(self):
        return "%s-%s" % (self.language.iso_2_code, self.translation.symbol)


class Book(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name='books')
    book_num = models.IntegerField()
    chapter_count = models.IntegerField()
    has_audio = models.BooleanField()

    standard_name = models.CharField(max_length=50)
    standard_abbr = models.CharField(max_length=50)
    official_abbr = models.CharField(max_length=50)

    standard_singular_name = models.CharField(max_length=50)
    standard_singular_abbr = models.CharField(max_length=50)
    official_singular_abbr = models.CharField(max_length=50)

    standard_plural_name = models.CharField(max_length=50)
    standard_plural_abbr = models.CharField(max_length=50)
    official_plural_abbr = models.CharField(max_length=50)

    url_segment = models.SlugField(max_length=50)

    class Meta:
        ordering = ('edition', 'book_num')
        unique_together = (
            ("edition", "book_num"),
        )

    def __str__(self):
        return self.standard_name


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    chapter_num = models.IntegerField()

    class Meta:
        ordering = (
            'book__edition',
            'book__book_num',
            'chapter_num',
        )
        unique_together = (
            ("book", "chapter_num"),
        )

    @property
    def book_name(self):
        return self.book.standard_name

    @property
    def citation(self):
        verses = self.verses.order_by('verse_num')
        return "%s %s:%s–%s" % (self.book_name, self.chapter_num, verses.first().verse_num, verses.last().verse_num)

    def __str__(self):
        return "%s %s" % (self.book.standard_name, self.chapter_num)


class Footnote(models.Model):
    edition = models.ForeignKey(Edition, on_delete=models.CASCADE, related_name='footnotes')
    fnid = models.SlugField(max_length=50)
    content = models.TextField()

    class Meta:
        ordering = ('edition', 'fnid')
        unique_together = (
            ("edition", "fnid"),
        )

    @property
    def text(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        return soup.find('span').text

    def __str__(self):
        return "%s - %s" % (self.fnid, self.text)


class Verse(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='verses')
    verse_num = models.IntegerField()
    content = models.TextField()
    footnotes = models.ManyToManyField(Footnote, related_name='verses')
    related_verses = models.ManyToManyField('self', through='VerseRelationship', symmetrical=False)

    class Meta:
        ordering = (
            'chapter__book__edition',
            'chapter__book__book_num',
            'chapter__chapter_num',
            'verse_num',
        )
        unique_together = (
            ("chapter", "verse_num"),
        )

    @classmethod
    def build_id(cls, book_num, chapter_num, verse_num):
        return str(book_num).zfill(2) + str(chapter_num).zfill(3) + str(verse_num).zfill(3)

    @classmethod
    def parse_id(cls, vsid):
        vsid = vsid.lstrip('v')
        return VerseID(
            book_num=int(vsid[:-6]),
            chapter_num=int(vsid[-6:-3]),
            verse_num=max(1, int(vsid[-3:])))

    @classmethod
    def parse_range(cls, vsrange):
        if not vsrange:
            return []

        vsrange = vsrange.split(',')
        verses = []
        for segment in vsrange:
            if '-' in segment:
                start, end = segment.split('-')
                start, end = cls.parse_id(start), cls.parse_id(end)
                for book in range(start.book_num, end.book_num + 1):
                    for chapter in range(start.chapter_num, end.chapter_num + 1):
                        for verse in range(start.verse_num, end.verse_num + 1):
                            verses.append(VerseID(
                                book_num=book,
                                chapter_num=chapter,
                                verse_num=verse))
            else:
                verses.append( cls.parse_id(segment) )
        return verses

    @classmethod
    def find_by_id(cls, edition, vsid):
        vsid = vsid if hasattr(vsid, 'book_num') else cls.parse_id(vsid)
        return cls.objects.get(
            chapter__book__edition=edition,
            chapter__book__book_num=vsid.book_num,
            chapter__chapter_num=vsid.chapter_num,
            verse_num=vsid.verse_num)

    @property
    def book_name(self):
        return self.chapter.book.standard_name

    @property
    def chapter_num(self):
        return self.chapter.chapter_num

    @property
    def citation(self):
        return "%s %s:%s" % (self.book_name, self.chapter_num, self.verse_num)

    @property
    def text(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        [n.extract() for n in soup.find_all('sup', class_="verseNum")]
        [n.extract() for n in soup.find_all('span', class_="chapterNum")]
        [n.extract() for n in soup.find_all('a')]
        return soup.text

    @property
    def marginal_refs(self):
        for r in self.sourced_relations.filter(relationship_type__code=VerseRelationshipType.T_XREF).all():
            yield r.to_verse

    def __str__(self):
        return "%s %s:%s" % (
            self.chapter.book.standard_name,
            self.chapter.chapter_num,
            self.verse_num)


class VerseRelationshipType(models.Model):
    T_XREF = 'xref'

    name = models.CharField(max_length=50)
    code = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class VerseRelationship(models.Model):
    relationship_type = models.ForeignKey(VerseRelationshipType, on_delete=models.CASCADE, related_name='relationships')
    from_verse = models.ForeignKey(Verse, on_delete=models.CASCADE, related_name='sourced_relations')
    to_verse = models.ForeignKey(Verse, on_delete=models.CASCADE, related_name='referenced_relations')

    class Meta:
        ordering = (
            'from_verse__chapter__book__edition',
            'from_verse__chapter__book__book_num',
            'from_verse__chapter__chapter_num',
            'from_verse__verse_num',
            'to_verse__chapter__book__edition',
            'to_verse__chapter__book__book_num',
            'to_verse__chapter__chapter_num',
            'to_verse__verse_num',
            'relationship_type__name',
        )
        unique_together = (
            ("relationship_type", "from_verse", "to_verse"),
        )

    def __str__(self):
        return "%s => %s" % (self.from_verse, self.to_verse)
