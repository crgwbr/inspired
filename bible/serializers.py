from rest_framework import serializers
from . import models


class Language(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Language
        fields = ('url', 'id', 'iso_2_code', 'wt_code', 'name')


class Translation(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Translation
        fields = ('url', 'id', 'symbol')


class Edition(serializers.HyperlinkedModelSerializer):
    symbol = serializers.CharField(source='translation.symbol')

    class Meta:
        model = models.Edition
        fields = ('url', 'id', 'language', 'translation', 'symbol', 'title')


class Book(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Book
        fields = (
            'url',
            'id',
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
        )


class Chapter(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Chapter
        fields = ('url', 'id', 'book', 'book_name', 'chapter_num', 'citation')


class Footnote(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Footnote
        fields = ('url', 'id', 'edition', 'fnid', 'content')


class VerseRelationshipType(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.VerseRelationshipType


class FootnoteCompact(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Footnote
        fields = ('fnid', 'content')


class VerseCompact(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Verse
        fields = (
            'url',
            'id',
            'citation',
            'content'
        )


class Verse(serializers.HyperlinkedModelSerializer):
    marginal_refs = VerseCompact(many=True)
    footnotes = FootnoteCompact(many=True)

    class Meta:
        model = models.Verse
        fields = (
            'url',
            'id',
            'citation',
            'content',
            'footnotes',
            'marginal_refs',
        )
