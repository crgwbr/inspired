'use strict';

var Collection = require("models/BaseCollection"),
    Editions;

Editions = Collection.extend({
    model: require('models/Edition'),
    urlBase: '/api/editions/',
});

module.exports = Editions;
