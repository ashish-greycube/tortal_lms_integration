# -*- coding: utf-8 -*-
# Copyright (c) 2018, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import unittest
import os
from frappe import _
from frappe.model.document import Document
import ftplib
import csv
from six import text_type
from six.moves.urllib.parse import urlparse, parse_qs
from frappe.utils import cint, split_emails
from frappe.utils.background_jobs import enqueue

class TortalLMSSystemSettings(Document):
	pass

def take_uploads_hourly():
	take_uploads_if("Hourly")

def take_uploads_if(freq):
	if cint(frappe.db.get_value("Tortal LMS System Settings", None, "is_integration_active")):
		upload_frequency = frappe.db.get_value("Tortal LMS System Settings", None, "frequency")
		if freq == "Hourly" and upload_frequency in ["Every 6 Hours","Every 12 Hours"]:
			last_upload_date = frappe.db.get_value('Tortal LMS System Settings', None, 'last_upload_date')
			if upload_frequency == "Every 6 Hours":
				upload_interval = 6
			elif upload_frequency == "Every 12 Hours":
				upload_interval = 12
		
			if datetime.now() - get_datetime(last_upload_date) >= timedelta(hours = upload_interval):
				take_upload_to_tortal()	

@frappe.whitelist()
def take_upload_to_tortal():
	try:
		upload_to_tortal()
		send_email(True, "Tortal LMS System Settings")
	except Exception:
		error_message = frappe.get_traceback()
		frappe.errprint(error_message)
		send_email(False, "Tortal LMS System Settings", error_message)


def send_email(success, service_name, error_status=None):
	if success:
		if frappe.db.get_value("Tortal LMS System Settings", None, "send_email_for_successful_upload") == '0':
			return

		subject = "Tortal FTP Upload Successful"
		message = """<h3>Backup Uploaded Successfully! </h3><p>Hi there, this is just to inform you
		that your files were successfully uploaded to Tortal system. So relax!</p> """

	else:
		subject = "[Warning] Tortal FTP Upload Failed"
		message = """<h3>Upload Failed! </h3><p>Oops, your automated upload to Tortal system failed.
		</p> <p>Error message: %s</p> <p>Please contact your system manager
		for more information.</p>""" % error_status

	if not frappe.db:
		frappe.connect()

	if frappe.db.get_value("Tortal LMS System Settings", None, "notification_email"):
		recipients = split_emails(frappe.db.get_value("Tortal LMS System Settings", None, "notification_email"))
		frappe.sendmail(recipients=recipients, subject=subject, message=message)


@frappe.whitelist()
def create_group_user_csv():
	group_user_data = frappe.db.sql("""select value from `tabSingles` where doctype='Tortal LMS System Settings' 
	and field in ('','','')""",as_list=1)
	row=[]
	row.append(frappe.db.get_value("Tortal LMS System Settings", None, "emp_identifier"))
	row.append(frappe.db.get_value("Tortal LMS System Settings", None, "group_name"))
	row.append(frappe.db.get_value("Tortal LMS System Settings", None, "group_admin"))
	print row
	with open('tortal_group_user_import_template.csv', 'wb') as f_handle:
		writer = csv.writer(f_handle)
		# Add the header/column names
		header = ['EmpIdentifier', 'GroupName', 'GroupAdmin']
		writer.writerow(header)
		writer.writerow(row)

@frappe.whitelist()
def create_tortal_user_csv():
	user_row=[]

	user_details=frappe.db.sql("""select name as username,first_name,middle_name,last_name,email,username,tortal_lms_password,frappe_userid,is_active_tortal_lms_user
									from `tabUser` 
									where is_active_tortal_lms_user=1 """,as_list=1)
	user_row.append(user_details)

	user_company_name=frappe.db.sql("""select customer_name 
										from `tabCustomer`inner join `tabUser` on (
										`tabCustomer`.name=`tabUser`.full_name)
										where `tabUser`.name=%s""",username,as_list=1)
	user_row.append(user_company_name)

	user_address=frappe.db.sql("""select `tabAddress`.address_line1,`tabAddress`.address_line2,`tabAddress`.city,`tabAddress`.state,`tabAddress`.pincode  
									FROM
										`tabDynamic Link`	
										inner join `tabAddress` on (
											`tabAddress`.name=`tabDynamic Link`.parent
										)
									where
										`tabDynamic Link`.link_name=%s and
										`tabDynamic Link`.docstatus=0 
										ORDER BY
										`tabAddress`.is_primary_address asc,
										`tabAddress`.creation asc
										LIMIT 1""",username,as_list=1)
	user_row.append(user_address)

	print user_row
	with open('tortal_user_import_template.csv', 'wb') as f_handle:
		writer = csv.writer(f_handle)
		# Add the header/column names
		header = ['First Name','Middle Name','Last Name','Email','Username','Password','Company','Address1','Address2','City','State','Postal Code','Identifier','IsActive']
		writer.writerow(header)
		writer.writerow(user_row)


def ftp_connect():
	IP=frappe.db.get_value("Tortal LMS System Settings", None, "ftp_address")
	ftpuser=frappe.db.get_value("Tortal LMS System Settings", None, "ftp_username")
	ftppwd=frappe.db.get_value("Tortal LMS System Settings", None, "ftp_password")
	print IP
	print ftpuser
	print ftppwd
	ftp = ftplib.FTP(IP)
	ftp.login(user=ftpuser, passwd = ftppwd)
	return ftp

def upload(ftp, filename,path=None):
	localfile = open(filename, 'wb')
	ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
	ftp.quit()
	localfile.close()

@frappe.whitelist()
def generate_tortal_link(username):
	result = frappe.db.sql("""select is_active_tortal_lms_user,username from `tabUser` where name=%s""",username,as_list=1)
	is_active_tortal_lms_user=result[0][0]
	username=result[0][1]
	if is_active_tortal_lms_user==1:
		tortal_sso_url=frappe.db.get_value("Tortal LMS System Settings", None, "tortal_sso_url")
		guid=frappe.db.get_value("Tortal LMS System Settings", None, "guid")
		tortal_link=tortal_sso_url+guid+'&username='+username
		return tortal_link
	else:
		return 'non-active-user'	
