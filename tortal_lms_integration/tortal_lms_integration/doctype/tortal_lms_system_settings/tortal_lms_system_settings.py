# -*- coding: utf-8 -*-
# Copyright (c) 2018, GreyCube Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import os
from frappe import _
from frappe.model.document import Document
import ftplib
import csv
from frappe.utils import cint, split_emails, get_site_base_path, cstr, today,get_backups_path,get_datetime,get_bench_path,get_files_path
from six import text_type
from datetime import datetime, timedelta
from frappe.utils.background_jobs import enqueue

class TortalLMSSystemSettings(Document):
	pass

def take_uploads_hourly():
	take_uploads_if("Hourly")

def take_uploads_daily():
	take_uploads_if("Daily")


def take_uploads_weekly():
	take_uploads_if("Weekly")

def take_uploads_if(freq):
	if cint(frappe.db.get_value("Tortal LMS System Settings", None, "is_integration_active")):
		upload_frequency = frappe.db.get_value("Tortal LMS System Settings", None, "frequency")
		if upload_frequency == freq:
			take_upload_to_tortal()
		elif freq == "Hourly" and upload_frequency in ["Every 6 Hours","Every 12 Hours"]:
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
		group_user_filename='tortal_group_user_import_template.csv'
		user_filename='tortal_user_import_template.csv'
		file_group_user_csv=create_tortal_group_user_csv(group_user_filename)
		file_tortal_user_csv=create_tortal_user_csv(user_filename)
		ftp=ftp_connect()
		upload_to_tortal(ftp,group_user_filename,file_group_user_csv)
		upload_to_tortal(ftp,user_filename,file_tortal_user_csv)
		ftp.quit()
		send_email(True, "Tortal LMS System Settings")
		frappe.db.begin()
		frappe.db.set_value('Tortal LMS System Settings', 'Tortal LMS System Settings', 'last_upload_date', datetime.now())
		frappe.db.commit()
	except Exception:
		error_message = frappe.get_traceback()
		frappe.errprint(error_message)
		send_email(False, "Tortal LMS System Settings", error_message)


def send_email(success, service_name, error_status=None):
	if success:
		if frappe.db.get_value("Tortal LMS System Settings", None, "send_email_for_successful_upload") == '0':
			return

		subject = "Tortal FTP Upload Successful"
		message = """<h3>Backup Uploaded Successfully! on %s</h3><p>Hi there, this is just to inform you
		that your files were successfully uploaded to Tortal system. So relax!</p> """% (datetime.now())

	else:
		subject = "[Warning] Tortal FTP Upload Failed"
		message = """<h3>Upload Failed! on %s </h3><p>Oops, your automated upload to Tortal system failed.
		</p> <p>Error message: %s</p> <p>Please contact your system manager
		for more information.</p>""" % (datetime.now(),error_status)

	if not frappe.db:
		frappe.connect()

	if frappe.db.get_value("Tortal LMS System Settings", None, "notification_email"):
		recipients = split_emails(frappe.db.get_value("Tortal LMS System Settings", None, "notification_email"))
		frappe.sendmail(recipients=recipients, subject=subject, message=message)


def create_tortal_group_user_csv(filename):
	row=[]
	row.append(frappe.db.get_value("Tortal LMS System Settings", None, "emp_identifier"))
	row.append(frappe.db.get_value("Tortal LMS System Settings", None, "group_name"))
	row.append(frappe.db.get_value("Tortal LMS System Settings", None, "group_admin"))

	private_files = get_files_path().replace("/public/", "/private/")
	private_files_path=get_bench_path()+"/sites"+private_files.replace("./", "/")

	with open(private_files_path+'/'+filename, 'wb') as f_handle:
		writer = csv.writer(f_handle)
		# Add the header/column names
		header = ['EmpIdentifier', 'GroupName', 'GroupAdmin']
		writer.writerow(header)
		writer.writerow(row)
	return os.path.realpath(f_handle.name)


def create_tortal_user_csv(filename):

	user_details=frappe.db.sql("""select t.first_name, t.middle_name, t.last_name, t.email, t.username, t.tortal_lms_password,
	   t.customer_name,t.address_line1,t.address_line2,t.city,t.state,t.pincode,t.frappe_userid,t.is_active_tortal_lms_user 
from ( select      @row_number:=CASE
		WHEN @customer_no = full_name THEN @row_number + 1
        ELSE 1
    	END AS num,
    	@customer_no:=full_name as CustomerNumber,
		full_name, first_name,middle_name,last_name,email,username,tortal_lms_password,frappe_userid,is_active_tortal_lms_user,
    	dl.parent, addr.address_line1,addr.address_line2,addr.city,addr.state,addr.pincode,cus.customer_name,
			case when addr.is_primary_address=1 then 1 else 0 end ord, coalesce(addr.creation, '1900-01-01') creation
			from `tabUser` usr
			left outer join `tabCustomer` cus on cus.name = usr.full_name
			left outer join `tabDynamic Link` dl on dl.parenttype='Address' 
			and dl.link_doctype='Customer' and dl.link_name=usr.full_name
			left outer join tabAddress addr on addr.name = dl.parent,(SELECT @customer_no:=0,@row_number:=0) as k
	) t where t.num = 1 and t.is_active_tortal_lms_user=1""",as_list=1)
	private_files = get_files_path().replace("/public/", "/private/")
	private_files_path=get_bench_path()+"/sites"+private_files.replace("./", "/")

	with open(private_files_path+'/'+filename, 'wb') as f_handle:
		writer = csv.writer(f_handle)
		# Add the header/column names
		header = ['First Name','Middle Name','Last Name','Email','Username','Password','Company','Address1','Address2','City','State','Postal Code','Identifier','IsActive']
		writer.writerow(header)
		for row in user_details:
			writer.writerow(row)
	return os.path.realpath(f_handle.name)

def ftp_connect():
	IP=frappe.db.get_value("Tortal LMS System Settings", None, "ftp_address")
	ftpuser=frappe.db.get_value("Tortal LMS System Settings", None, "ftp_username")
	ftppwd=frappe.db.get_value("Tortal LMS System Settings", None, "ftp_password")
	ftp = ftplib.FTP(IP)
	ftp.login(user=ftpuser, passwd = ftppwd)
	return ftp

def upload_to_tortal(ftp, filename,path):
	localfile = open(path, 'rb')
	ftp.storbinary('STOR '+filename, localfile)
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