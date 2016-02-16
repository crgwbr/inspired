'use strict';

var Backbone = require('backbone'),
    BaseModel = require('models/BaseModel'),
    Footnotes = require('models/Footnotes'),
    MarginalRefs, Verse;


Verse = BaseModel.extend({
    parse: function(data) {
        data.marginal_refs = new MarginalRefs(data.marginal_refs);
        data.footnotes = new Footnotes(data.footnotes);
        return data;
    }
});


MarginalRefs = Backbone.Collection.extend({
    model: Verse,
    url: '/api/verses/',
});


module.exports = Verse;
