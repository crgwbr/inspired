'use strict';
var Marionette = require('backbone.marionette'),
    $ = require('jquery'),
    // _ = require('underscore'),
    ViewportStick;


ViewportStick = Marionette.Behavior.extend({
    ui: {
        anchor: '.viewport-stick-anchor',
        elem: '.viewport-stick',
    },

    onRender: function() {
        var self = this;

        this.onScroll = function() {
            var windowTop = $(window).scrollTop();

            self.view.$el.find('.viewport-stick').each(function() {
                var elem = $(this),
                    divTop = elem.prev('.viewport-stick-anchor').offset().top;

                elem.css('top', Math.max(0, windowTop - divTop));
            });
        };

        $(window).on('scroll', this.onScroll);

        setTimeout(function() {
            self.onScroll();
            self.view.$el.find('.viewport-stick').addClass('viewport-stick-loaded');
        }, 200);
    },


    onBeforeDestroy: function() {
        $(window).off('scroll', this.onScroll);
    }
});

module.exports = ViewportStick;
