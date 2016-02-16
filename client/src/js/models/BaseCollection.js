'use strict';

var PageableCollection = require("backbone.paginator"),
    $ = require('jquery'),
    BaseCollection;

BaseCollection = PageableCollection.extend({
    mode: "server",

    state: {
        firstPage: 1,
        pageSize: 100,
    },

    queryParams: {
        currentPage: "page",
        pageSize: null,
    },

    initialize: function() {
        this.filter = {};
        PageableCollection.prototype.initialize.apply(this, arguments);
    },

    parseRecords: function(resp) {
        return resp.results;
    },

    parseState: function(resp) {
        return {
            totalRecords: resp.count,
        };
    },

    setFilter: function(param, value) {
        this.filter[param] = value;
    },

    url: function() {
        return this.urlBase + '?' + $.param(this.filter);
    }
});

module.exports = BaseCollection;
