'use strict';
var Backbone = require('backbone'),
    _ = require('underscore'),
    BaseModel;

BaseModel = Backbone.Model.extend({
    relationships: {},
    _rcache: {},

    get: function(prop) {
        var def = this.relationships[prop],
            self = this,
            container;

        if (!def) {
            return Backbone.Model.prototype.get.apply(this, arguments);
        }

        if (this._rcache[prop]) {
            return this._rcache[prop];
        }

        container = new def.Container();
        _.each(def.filters, function(prop, param) {
            container.setFilter(param, self.get(prop));
        });
        return container;
    }
});

module.exports = BaseModel;
