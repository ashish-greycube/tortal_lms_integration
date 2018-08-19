# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "tortal_lms_integration"
app_title = "Tortal LMS Integration"
app_publisher = "GreyCube Technologies"
app_description = "Provide single sign on (SSO) for ERPNext user to Tortal LMS system"
app_icon = "octicon octicon-key"
app_color = "#0079bb"
app_email = "admin@greycube.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/tortal_lms_integration/css/tortal_lms_integration.css"
# app_include_js = "/assets/tortal_lms_integration/js/tortal_lms_integration.js"

# include js, css files in header of web template
# web_include_css = "/assets/tortal_lms_integration/css/tortal_lms_integration.css"
web_include_js = "/assets/tortal_lms_integration/js/tortal_lms_integration.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "tortal_lms_integration.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "tortal_lms_integration.install.before_install"
# after_install = "tortal_lms_integration.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "tortal_lms_integration.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"tortal_lms_integration.tasks.all"
	# ],
	# "daily": [
	# 	"tortal_lms_integration.tasks.daily"
	# ],
	"hourly": [
		"tortal_lms_integration.tortal_lms_integration.doctype.tortal_lms_system_settings.tortal_lms_system_settings.take_uploads_hourly"
	],
	# "weekly": [
	# 	"tortal_lms_integration.tasks.weekly"
	# ]
	# "monthly": [
	# 	"tortal_lms_integration.tasks.monthly"
	# ]
}

# Testing
# -------

# before_tests = "tortal_lms_integration.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "tortal_lms_integration.event.get_events"
# }

