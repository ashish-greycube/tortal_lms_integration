// Copyright (c) 2018, GreyCube Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tortal LMS System Settings', {
	refresh: function(frm) {
		frm.clear_custom_buttons();
		frm.events.take_upload(frm);
	},

	take_upload: function(frm) {
		if (frm.doc.ftp_address && frm.doc.ftp_username && frm.doc.ftp_password && frm.doc.is_integration_active==1 ) {
			frm.add_custom_button(__("Uploadp Now"), function(){
				frm.dashboard.set_headline_alert("Tortal Upload Started!");
				frappe.call({
					method: "tortal_lms_integration.tortal_lms_integration.doctype.tortal_lms_system_settings.tortal_lms_system_settings.take_upload_to_tortal",
					callback: function(r) {
						if(!r.exc) {
							frappe.msgprint(__("Tortal Upload complete!"));
							frm.dashboard.clear_headline();
						}
					}
				});
			}).addClass("btn-primary");
		}
	}
});
