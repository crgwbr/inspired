'use strict';
var Marionette = require('backbone.marionette'),
    Backbone = require('backbone'),
    EditionSelector = require('views/EditionSelector'),
    ChapterSelector = require('views/ChapterSelector'),
    ChapterSetView = require('views/ChapterSet'),
    Root;


Root = Marionette.LayoutView.extend({
    template: "root.html",
    className: "view-root",

    regions: {
        editionSelector: 'div.edition-selector',
        chapterSelector: 'div.chapter-selector',
        content: 'div.content',
    },

    events: {
    },


    initialize: function() {
        this.model = new Backbone.Model();
        this.chapters = new Backbone.Collection();
    },


    onRender: function() {
        this.renderEditionSelector();

        this.showChildView('content', new ChapterSetView({
            collection: this.chapters
        }));
    },


    renderEditionSelector: function() {
        var view = new EditionSelector({ model: this.model });
        view.on('change:edition', this.renderChapterSelector.bind(this));
        this.showChildView('editionSelector', view);
    },


    renderChapterSelector: function(edition) {
        var view = new ChapterSelector({ model: this.model, edition: edition });
        view.on('change:chapter', this.renderChapter.bind(this));
        this.showChildView('chapterSelector', view);
    },


    renderChapter: function(chapter) {
        this.chapters.reset();
        this.chapters.add(chapter);
    },
});


module.exports = Root;
