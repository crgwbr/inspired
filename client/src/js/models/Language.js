'use strict';

var BaseModel = require('models/BaseModel'),
    Language;

Language = BaseModel.extend({
    idAttribute: 'iso_2_code',
    relationships: {
        editions: {
            Container: require('models/Editions'),
            filters: {
                'language': 'id',
            }
        }
    }
});

module.exports = Language;
