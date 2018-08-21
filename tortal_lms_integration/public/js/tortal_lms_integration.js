// To be placed in script section of web page with route training-portal
$(function () {
    window.full_name = getCookie("full_name");
    var logged_in = getCookie("sid") && getCookie("sid") !== "Guest";
    if (window.location.pathname == '/training-portal') {
        if (logged_in == false) {
            frappe.msgprint("<b>Please purchase training plan</b>", 'Access Denied')
            window.setTimeout(function () {
                window.location = "/";
            }, 2000);
        } else {
            var user_role
            frappe.call({
                method: 'tortal_lms_integration.tortal_lms_integration.doctype.tortal_lms_system_settings.tortal_lms_system_settings.generate_tortal_link',
                args: {
                    username: frappe.session.user
                },
                callback: function (r) {
                    tortal_link = r.message
                    if (tortal_link == 'non-active-user') {
                        frappe.msgprint("<b>Please purchase training plans</b>", 'Access Denied')
                        window.setTimeout(function () {
                            window.location = "/";
                        }, 2000);
                    } else {
                        $("a[href='http://empowery.tortal.net']").attr('href', tortal_link)
                    }
                }
            })
        }
    }
});
// HTML code for web page
// <div><a class="tortal" href="http://empowery.tortal.net" target="_blank"><b><span style="font-size: 18px;">Empowery Learning Management System</span></b></a><br></div>