'use strict';

var BaseModel = require('models/BaseModel'),
    Edition;

Edition = BaseModel.extend({
    idAttribute: 'symbol',
    relationships: {
        books: {
            Container: require('models/Books'),
            filters: {
                'edition': 'id',
            }
        }
    }
});

module.exports = Edition;
