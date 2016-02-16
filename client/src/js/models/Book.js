'use strict';

var BaseModel = require('models/BaseModel'),
    Book;

Book = BaseModel.extend({
    idAttribute: 'book_num',
    relationships: {
        chapters: {
            Container: require('models/Chapters'),
            filters: {
                'book': 'id',
            }
        }
    }
});

module.exports = Book;
