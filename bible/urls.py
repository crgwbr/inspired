from django.conf.urls import url, include
from rest_framework import routers
from . import viewsets, views



router = routers.DefaultRouter()
router.register(r'languages', viewsets.Language)
router.register(r'translations', viewsets.Translation)
router.register(r'editions', viewsets.Edition)
router.register(r'books', viewsets.Book)
router.register(r'chapters', viewsets.Chapter)
router.register(r'footnotes', viewsets.Footnote)
router.register(r'verses', viewsets.Verse)
router.register(r'verse-relationship-types', viewsets.VerseRelationshipType)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^', views.RootView.as_view()),
]
