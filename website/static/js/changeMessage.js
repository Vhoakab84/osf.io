'use strict';
var ko = require('knockout');
var oop = require('js/oop');
/** Change the flashed status message */

var changeMessage = oop.defclass({
    constructor: function() {
        this.message = ko.observable('');
        this.messageClass = ko.observable('text-info');
    },
    changeMessage: function(text, css, timeout) {
        var self = this;
        if (typeof text === 'function') {
            text = text();
        }
        self.message(text);
        var cssClass = css || 'text-info';
        self.messageClass(cssClass);
        if (timeout) {
            // Reset message after timeout period
            setTimeout(function () {
                self.message('');
                self.messageClass('text-info');
            }, timeout);
        }
    }
});

module.exports = changeMessage;
