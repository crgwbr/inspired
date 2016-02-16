'use strict';

var BaseModel = require('models/BaseModel'),
    Chapter;

Chapter = BaseModel.extend({
    idAttribute: 'chapter_num',
    relationships: {
        verses: {
            Container: require('models/Verses'),
            filters: {
                'chapter': 'id',
            }
        }
    }
});

module.exports = Chapter;
