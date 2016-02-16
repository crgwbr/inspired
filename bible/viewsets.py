from rest_framework import viewsets, response, decorators
from . import models, serializers, permissions, filters


class Language(viewsets.ModelViewSet):
    queryset = models.Language.objects.all()
    serializer_class = serializers.Language


class Translation(viewsets.ModelViewSet):
    queryset = models.Translation.objects.all()
    serializer_class = serializers.Translation


class Edition(viewsets.ModelViewSet):
    queryset = models.Edition.objects.all()
    serializer_class = serializers.Edition
    permission_classes = (permissions.ReadOnly, )
    filter_class = filters.Edition

    @decorators.detail_route(methods=['get'])
    def books(self, request, pk=None):
        books = models.Book.objects.filter(edition__id=pk)
        ser = serializers.Book(books, many=True, context={'request': request})
        return response.Response(ser.data)


class Book(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.Book
    permission_classes = (permissions.ReadOnly, )
    filter_class = filters.Book


class Chapter(viewsets.ModelViewSet):
    queryset = models.Chapter.objects.all()
    serializer_class = serializers.Chapter
    permission_classes = (permissions.ReadOnly, )
    filter_class = filters.Chapter


class Footnote(viewsets.ModelViewSet):
    queryset = models.Footnote.objects.all()
    serializer_class = serializers.Footnote
    permission_classes = (permissions.ReadOnly, )
    filter_class = filters.Footnote


class Verse(viewsets.ModelViewSet):
    queryset = models.Verse.objects.all()
    serializer_class = serializers.Verse
    permission_classes = (permissions.ReadOnly, )
    filter_class = filters.Verse


class VerseRelationshipType(viewsets.ModelViewSet):
    queryset = models.VerseRelationshipType.objects.all()
    serializer_class = serializers.VerseRelationshipType
