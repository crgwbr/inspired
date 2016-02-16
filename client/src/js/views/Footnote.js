'use strict';
var Marionette = require('backbone.marionette'),
    Footnote;


Footnote = Marionette.ItemView.extend({
    template: "footnote.html",
    className: "view-footnote",

    behaviors: {
        ViewportStick: {},
    },

    templateHelpers: function() {
        return {
            citation: this.options.source.get('citation')
        };
    }
});

module.exports = Footnote;
