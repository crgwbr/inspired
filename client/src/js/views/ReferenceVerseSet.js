'use strict';
var Marionette = require('backbone.marionette'),
    ReferenceVerseSet;


ReferenceVerseSet = Marionette.CompositeView.extend({
    template: 'reference-verse-set.html',
    className: "view-reference-verse-set",
    childView: require('views/ReferenceVerse'),
    childViewContainer: '.refs',

    behaviors: {
        ViewportStick: {},
    },
});


module.exports = ReferenceVerseSet;
