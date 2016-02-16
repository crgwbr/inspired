'use strict';
var Marionette = require('backbone.marionette'),
    $ = require('jquery'),
    Verse;


Verse = Marionette.ItemView.extend({
    template: "verse.html",
    tagName: 'span',
    className: "view-verse",

    events: {
        'click .verseNum a': 'noop',
        'click .chapterNum a': 'noop',

        'click .footnote': 'showFootnote',
        'click .marginal-ref': 'showMarginalReference',

        'mouseover .footnote': 'showFootnote',
        'mouseover .marginal-ref': 'showMarginalReference',

        'mouseleave .footnote': 'unfocus',
        'mouseleave .marginal-ref': 'unfocus',
    },

    noop: function(e) {
        e.preventDefault();
    },

    unfocus: function(e) {
        e.preventDefault();
        this.trigger('unfocusVerse');
    },

    showFootnote: function(e) {
        e.preventDefault();
        var fnid = $(e.target).attr('href').replace('#', ''),
            footnotes = this.model.get('footnotes'),
            footnote = footnotes.get(fnid);

        this.trigger('show:footnote', this.model, footnote);
    },

    showMarginalReference: function(e) {
        e.preventDefault();
        var verses = $(e.target).data('verses'),
            refs = this.model.get('marginal_refs'),
            subset = refs.clone();

        subset.reset(refs.filter(function(v) {
            return verses.indexOf(v.id) !== -1;
        }));

        this.trigger('show:relatedVerseSet', this.model, subset);
    }
});

module.exports = Verse;
