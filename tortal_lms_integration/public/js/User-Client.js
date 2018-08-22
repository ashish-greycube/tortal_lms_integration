frappe.ui.form.on("User", {
    is_active_tortal_lms_user: function (frm, cdt, cdn) {
        frm.set_df_property('username', 'reqd', frm.doc.is_active_tortal_lms_user == 1);
        if (frm.doc.is_active_tortal_lms_user == 1) {
            var length = 8,
                charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
                retVal = "";
            for (var i = 0, n = charset.length; i < length; ++i) {
                retVal += charset.charAt(Math.floor(Math.random() * n));
            }
            frm.set_value('tortal_lms_password', retVal)
            if ($("[data-user-role='Tortal LMS']").find('input[type=checkbox]').is(":checked") == false) {
                $("[data-user-role='Tortal LMS']").find('input[type=checkbox]').trigger('click')
            }
        }
        if (frm.doc.is_active_tortal_lms_user == 0) {
            if ($("[data-user-role='Tortal LMS']").find('input[type=checkbox]').is(":checked") == true) {
                $("[data-user-role='Tortal LMS']").find('input[type=checkbox]').trigger('click')
            }
        }
    }
});