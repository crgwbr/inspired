'use strict';

var Collection = require("models/BaseCollection"),
    Footnotes;

Footnotes = Collection.extend({
    model: require('models/Footnote'),
    urlBase: '/api/footnotes/',
});

module.exports = Footnotes;
