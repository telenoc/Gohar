odoo.define('web.custom_widget_color', function(require) {
    "use strict";

    var basic_fields = require('web.basic_fields');
    var field_registry = require('web.field_registry');

    var DynamicColor = basic_fields.FieldChar.extend({
        _renderEdit: function() {
            this._prepareInput(this.$el);
            this.$input = this.$el.find('input');
            this.$input.prevObject[0].type = 'color'
        },
        _setValue: function (value, options) {
             value = this.$input.prevObject[0].value;
            return this._super(value, options);
        },
    });
    field_registry.add('custom_color',DynamicColor);
});
