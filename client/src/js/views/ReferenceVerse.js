'use strict';
var VerseView = require('views/Verse'),
    ReferenceVerse;


ReferenceVerse = VerseView.extend({
    template: "reference-verse.html",
    tagName: 'div',
    className: "view-reference-verse",
});

module.exports = ReferenceVerse;
