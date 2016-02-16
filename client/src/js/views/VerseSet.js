'use strict';
var Marionette = require('backbone.marionette'),
    VerseSet;


VerseSet = Marionette.CollectionView.extend({
    className: "view-verse-set",
    childView: require('views/Verse'),
});


module.exports = VerseSet;
