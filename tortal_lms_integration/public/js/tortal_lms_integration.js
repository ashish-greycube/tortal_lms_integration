$(document).ready(function () {
    window.full_name = getCookie("full_name");
    var logged_in = getCookie("sid") && getCookie("sid") !== "Guest";
    console.log('1')
    // console.log(logged_in)
    // console.log(window.full_name)
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
                    // console.log(r.message)
                    tortal_link = r.message
                    console.log('4')
                    if (tortal_link == 'non-active-user') {
                        console.log('3')
                        frappe.msgprint("<b>Please purchase training plans</b>", 'Access Denied')
                        window.setTimeout(function () {
                            window.location = "/";
                        }, 2000);
                    }
                    else{
                        console.log('2')
                        $("a[href='http://empowery.tortal.net/']").attr('href', 'http://www.live.com/')
                        // $("[href='http://empowery.tortal.net/']").attr("href", tortal_link)
                    }
                }
            })
        }
    }

});