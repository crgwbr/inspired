from django.contrib import admin
from . import models


@admin.register(models.Language)
class Language(admin.ModelAdmin):
    fields = ['iso_2_code', 'wt_code', 'name', 'edition_api']
    list_display = ['iso_2_code', 'wt_code', 'name']


@admin.register(models.Translation)
class Translation(admin.ModelAdmin):
    fields = ['symbol']
    list_display = ['symbol']


@admin.register(models.Edition)
class Edition(admin.ModelAdmin):
    fields = ['language', 'translation', 'title', 'content_api']
    readonly_fields = fields
    list_display = ['title', 'language', 'translation']
    list_filter = ['language__name', 'translation__symbol']


@admin.register(models.Book)
class Book(admin.ModelAdmin):
    fields = [
        'edition',
        'book_num',
        'chapter_count',
        'has_audio',
        'standard_name',
        'standard_abbr',
        'official_abbr',
        'standard_singular_name',
        'standard_singular_abbr',
        'official_singular_abbr',
        'standard_plural_name',
        'standard_plural_abbr',
        'official_plural_abbr',
        'url_segment',
    ]
    readonly_fields = fields

    list_display = ['standard_name', 'edition', 'book_num', 'has_audio', 'url_segment']
    list_filter = ['edition__language__name', 'edition__translation__symbol', 'has_audio']
    search_fields = [
        'standard_name',
        'standard_abbr',
        'official_abbr',
        'standard_singular_name',
        'standard_singular_abbr',
        'official_singular_abbr',
        'standard_plural_name',
        'standard_plural_abbr',
        'official_plural_abbr',
        'url_segment',
    ]


@admin.register(models.Chapter)
class Chapter(admin.ModelAdmin):
    fields = ['book', 'chapter_num']
    readonly_fields = fields
    list_filter = ['book__edition__language__name', 'book__edition__translation__symbol']


@admin.register(models.Verse)
class Verse(admin.ModelAdmin):
    fields = ['chapter', 'verse_num', 'content', 'text', 'footnotes', 'related_verses']
    readonly_fields = fields
    list_filter = [
        'chapter__book__edition__language__name',
        'chapter__book__edition__translation__symbol',
        'chapter__book__has_audio'
    ]


@admin.register(models.Footnote)
class Footnote(admin.ModelAdmin):
    fields = ['edition', 'fnid', 'content', 'text']
    readonly_fields = fields
    list_display = ['fnid', 'text']
    search_fields = ['fnid', 'content']
    list_filter = [
        'edition__language__name',
        'edition__translation__symbol',
    ]


@admin.register(models.VerseRelationshipType)
class VerseRelationshipType(admin.ModelAdmin):
    list_display = ['name', 'code']


@admin.register(models.VerseRelationship)
class VerseRelationship(admin.ModelAdmin):
    fields = ['relationship_type', 'from_verse', 'to_verse']
    readonly_fields = fields
    list_display = ['from_verse', 'to_verse', 'relationship_type']
    list_filter = [
        'from_verse__chapter__book__edition__language__name',
        'from_verse__chapter__book__edition__translation__symbol',
        'relationship_type__name',
    ]
