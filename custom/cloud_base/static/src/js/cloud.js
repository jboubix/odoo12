odoo.define('cloud_base.cloud', function(require) {
"use strict";

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Sidebar = require('web.Sidebar');
    var rpc = require("web.rpc");
    var _t = core._t;

    Sidebar.include({
        _onDropdownClicked: function (event) {
            // Re-write to catch Cloud Client folder action
            if (event.currentTarget.name == "cloud_client") {
                var self = this;
                var aItem = $(event.target).parent();
                var resId = aItem.data("id");
                var resModel = aItem.data("model");
                this._rpc({
                        model: "ir.attachment",
                        method: 'open_cloud_folder',
                        args: [{
                            "res_model": resModel,
                            "res_id": resId,
                        }],
                    })
                    .then(function (res) {
                        if (res) {
                            self.do_action(res);
                        }
                        else {
                            self.do_warn(_t('The object is either not synced or the service is unavailable'));
                        }
                    });
            }
            else {
                this._super.apply(this, arguments);
            }
        },
    });

    return Sidebar;

});