'use strict';
var Marionette = require('backbone.marionette'),
    Languages = require('models/Languages'),
    Editions = require('models/Editions'),
    EditionSelector;


EditionSelector = Marionette.ItemView.extend({
    template: "edition-selector.html",
    className: "view-edition-selector",

    bindings: {
        'select.language': {
            observe: 'language',
            selectOptions: {
                collection: 'this.languages',
                labelPath: 'name',
                valuePath: 'iso_2_code'
            }
        },
        'select.edition': {
            observe: 'edition',
            selectOptions: {
                collection: 'this.editions',
                labelPath: 'title',
                valuePath: 'symbol'
            }
        },
    },

    initialize: function() {
        this.languages = new Languages();
        this.editions = new Editions();
    },

    loadEditions: function() {
        var language_id = this.model.get('language'),
            language = this.languages.get(language_id) || this.languages.first(),
            self = this,
            editions;

        if (!language) {
            return;
        }

        editions = language.get('editions');
        editions.fetch().then(function() {
            self.editions.reset(editions.models);
            self.sendChangeEvent();
        });
    },

    onRender: function() {
        this.stickit();

        this.model.on('change:language', this.loadEditions.bind(this));
        this.model.on('change:edition', this.sendChangeEvent.bind(this));
        this.languages.fetch().then( this.loadEditions.bind(this) );
    },

    getSelectedEdition: function() {
        var edition_id = this.model.get('edition'),
            edition = this.editions.get(edition_id);
        return edition || this.editions.first();
    },

    sendChangeEvent: function() {
        var edition = this.getSelectedEdition();
        if (edition.get('url') !== this._editionURL) {
            this._editionURL = edition.get('url');
            this.trigger('change:edition', edition);
        }
    }
});


module.exports = EditionSelector;
