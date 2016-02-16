'use strict';

var BaseModel = require('models/BaseModel'),
    Footnote;


Footnote = BaseModel.extend({
    idAttribute: 'fnid',
});


module.exports = Footnote;
