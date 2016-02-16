'use strict';
var Marionette = require('backbone.marionette'),
    VerseSet = require('views/VerseSet'),
    ReferenceVerseSet = require('views/ReferenceVerseSet'),
    Footnote = require('views/Footnote'),
    Chapter;


Chapter = Marionette.LayoutView.extend({
    template: "chapter.html",
    className: "view-chapter",

    regions: {
        verses: 'div.verses',
        references: 'div.references',
    },


    childEvents: {
        'childview:show:relatedVerseSet': 'showRelatedVerseSet',
        'childview:show:footnote': 'showFootnote',
        'childview:unfocusVerse': 'unfocusVerse',
    },


    onRender: function() {
        var verses = this.model.get('verses');
        verses.fetch();

        this.showChildView('verses', new VerseSet({
            collection: verses
        }));
    },

    showFootnote: function(verseSetView, verseView, source, footnote) {
        this.showChildView('references', new Footnote({
            source: source,
            model: footnote,
        }));
        this.focusVerse(verseView);
    },

    showRelatedVerseSet: function(verseSetView, verseView, source, verses) {
        this.showChildView('references', new ReferenceVerseSet({
            model: source,
            collection: verses
        }));
        this.focusVerse(verseView);
    },

    focusVerse: function(verseView) {
        clearTimeout(this._unfocusTimer);
        this.getRegion('verses').$el.find('.view-verse').addClass('dim').removeClass('focus');
        verseView.$el.removeClass('dim').addClass('focus');
    },

    unfocusVerse: function() {
        var self = this;
        this._unfocusTimer = setTimeout(function() {
            self.getRegion('verses').$el.find('.view-verse').removeClass('dim focus');
        }, 1000);
    }
});


module.exports = Chapter;
