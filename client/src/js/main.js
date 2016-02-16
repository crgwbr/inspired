'use strict';

var Backbone = require('backbone'),
    Marionette = require('backbone.marionette'),
    nunjucks = require('nunjucks'),
    $ = require('jquery'),
    RootView = require('views/Root'),
    templating;


// Register jQuery instance with Backbone
Backbone.$ = $;

// Install stickit plugin
require('backbone.stickit');

// Setup templating with Marionette
templating = (function() {
    var loader = nunjucks.WebLoader ? new nunjucks.WebLoader('/static') : undefined;
    return new nunjucks.Environment(loader);
}());

Marionette.Renderer.render = function(name, data) {
    return templating.render(name, data);
};

// Random widgets
Marionette.Behaviors.behaviorsLookup = function() {
    return {
        'ViewportStick': require('behaviors/ViewportStick'),
    };
};



// Setup and start the application
var app = new Marionette.Application();

app.on("start", function(options) {
    var view = new RootView(options);
    view.render();
});

app.start({
    el: $('#inspired-app')
});
