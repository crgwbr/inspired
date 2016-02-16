import django_filters
from rest_framework import filters
from . import models


class Edition(filters.FilterSet):
    language = django_filters.NumberFilter(name="language__id")
    language_code = django_filters.CharFilter(name="language__iso_2_code")

    translation = django_filters.NumberFilter(name="translation__id")
    translation_symbol = django_filters.CharFilter(name="translation__symbol")

    class Meta:
        model = models.Edition
        fields = (
            'language',
            'language_code',
            'translation',
            'translation_symbol',
        )


class Book(filters.FilterSet):
    language = django_filters.NumberFilter(name="edition__language__id")
    language_code = django_filters.CharFilter(name="edition__language__iso_2_code")

    translation = django_filters.NumberFilter(name="edition__translation__id")
    translation_symbol = django_filters.CharFilter(name="edition__translation__symbol")

    edition = django_filters.NumberFilter(name="edition__id")

    book_num = django_filters.NumberFilter(name="book_num")

    class Meta:
        model = models.Book
        fields = (
            'language',
            'language_code',
            'translation',
            'translation_symbol',
            'book_num',
        )


class Chapter(filters.FilterSet):
    language = django_filters.NumberFilter(name="book__edition__language__id")
    language_code = django_filters.CharFilter(name="book__edition__language__iso_2_code")

    translation = django_filters.NumberFilter(name="book__edition__translation__id")
    translation_symbol = django_filters.CharFilter(name="book__edition__translation__symbol")

    edition = django_filters.NumberFilter(name="edition__id")

    book = django_filters.NumberFilter(name="book__id")
    book_num = django_filters.NumberFilter(name="book__book_num")

    chapter_num = django_filters.NumberFilter(name="chapter_num")

    class Meta:
        model = models.Chapter
        fields = (
            'language',
            'language_code',
            'translation',
            'translation_symbol',
            'book',
            'book_num',
            'chapter_num',
        )


class Footnote(filters.FilterSet):
    language = django_filters.NumberFilter(name="edition__language__id")
    language_code = django_filters.CharFilter(name="edition__language__iso_2_code")

    translation = django_filters.NumberFilter(name="edition__translation__id")
    translation_symbol = django_filters.CharFilter(name="edition__translation__symbol")

    edition = django_filters.NumberFilter(name="edition__id")

    book = django_filters.NumberFilter(name="verses__chapter__book__id")
    book_num = django_filters.NumberFilter(name="verses__chapter__book__book_num")

    chapter = django_filters.NumberFilter(name="verses__chapter__id")
    chapter_num = django_filters.NumberFilter(name="verses__chapter__chapter_num")

    verse = django_filters.NumberFilter(name="verses__id")
    verse_num = django_filters.NumberFilter(name="verses__verse_num")

    class Meta:
        model = models.Footnote
        fields = (
            'language',
            'language_code',
            'translation',
            'translation_symbol',
            'book',
            'book_num',
            'chapter',
            'chapter_num',
            'verse',
            'verse_num',
        )


class Verse(filters.FilterSet):
    language = django_filters.NumberFilter(name="chapter__book__edition__language__id")
    language_code = django_filters.CharFilter(name="chapter__book__edition__language__iso_2_code")

    translation = django_filters.NumberFilter(name="chapter__book__edition__translation__id")
    translation_symbol = django_filters.CharFilter(name="chapter__book__edition__translation__symbol")

    edition = django_filters.NumberFilter(name="edition__id")

    book = django_filters.NumberFilter(name="chapter__book__id")
    book_num = django_filters.NumberFilter(name="chapter__book__book_num")

    chapter = django_filters.NumberFilter(name="chapter__id")
    chapter_num = django_filters.NumberFilter(name="chapter__chapter_num")

    verse_num = django_filters.NumberFilter(name="verse_num")

    class Meta:
        model = models.Verse
        fields = (
            'language',
            'language_code',
            'translation',
            'translation_symbol',
            'book',
            'book_num',
            'chapter',
            'chapter_num',
            'verse_num',
        )
