'use strict';
var Marionette = require('backbone.marionette'),
    Chapters = require('models/Chapters'),
    ChapterSelector;


ChapterSelector = Marionette.ItemView.extend({
    template: "chapter-selector.html",
    className: "view-chapter-selector",

    bindings: {
        'select.book': {
            observe: 'book',
            selectOptions: {
                collection: 'this.books',
                labelPath: 'standard_name',
                valuePath: 'book_num'
            }
        },
        'select.chapter': {
            observe: 'chapter',
            selectOptions: {
                collection: 'this.chapters',
                labelPath: 'chapter_num',
                valuePath: 'chapter_num'
            }
        }
    },

    initialize: function(options) {
        this.books = options.edition.get('books');
        this.chapters = new Chapters();
    },

    loadChapters: function() {
        var book_id = this.model.get('book'),
            book = this.books.get(book_id) || this.books.first(),
            self = this,
            chapters;

        if (!book) {
            return;
        }

        chapters = book.get('chapters');
        chapters.fetch().then(function() {
            self.chapters.reset(chapters.models);
            self.sendChangeEvent();
        });
    },

    onRender: function() {
        this.stickit();

        this.model.on('change:book', this.loadChapters.bind(this));
        this.model.on('change:chapter', this.sendChangeEvent.bind(this));
        this.books.fetch().then( this.loadChapters.bind(this) );
    },

    getSelectedChapter: function() {
        var chapter_id = this.model.get('chapter'),
            chapter = this.chapters.get(chapter_id);
        return chapter || this.chapters.first();
    },

    sendChangeEvent: function() {
        var chapter = this.getSelectedChapter();
        if (chapter.get('url') !== this._chapterURL) {
            this._chapterURL = chapter.get('url');
            this.trigger('change:chapter', chapter);
        }
    }
});


module.exports = ChapterSelector;
