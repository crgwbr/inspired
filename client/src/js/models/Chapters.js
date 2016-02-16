'use strict';

var Collection = require("models/BaseCollection"),
    Chapters;

Chapters = Collection.extend({
    model: require('models/Chapter'),
    urlBase: '/api/chapters/',
});

module.exports = Chapters;
