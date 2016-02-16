'use strict';

var Collection = require("models/BaseCollection"),
    Editions;

Editions = Collection.extend({
    model: require('models/Book'),
    urlBase: '/api/books/',
});

module.exports = Editions;
