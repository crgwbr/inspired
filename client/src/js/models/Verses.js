'use strict';

var Collection = require("models/BaseCollection"),
    Verses;

Verses = Collection.extend({
    model: require('models/Verse'),
    urlBase: '/api/verses/',
});

module.exports = Verses;
