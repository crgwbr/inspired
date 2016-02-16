'use strict';

var Collection = require("models/BaseCollection"),
    Languages;

Languages = Collection.extend({
    model: require('models/Language'),
    urlBase: '/api/languages/',
});

module.exports = Languages;
