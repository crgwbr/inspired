'use strict';
var Marionette = require('backbone.marionette'),
    ChapterSet;


ChapterSet = Marionette.CollectionView.extend({
    className: "view-chapter-set",
    childView: require('views/Chapter'),
});


module.exports = ChapterSet;
