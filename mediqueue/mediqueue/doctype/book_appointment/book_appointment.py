# Copyright (c) 2025, Krupalvora and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

frappe.utils.logger.set_log_level("DEBUG")
logger = frappe.logger("BookAppointment", allow_site=True)

class BookAppointment(Document):
    def before_insert(self):
        logger.debug("BookAppointment: " + str(self.start_time))
        logger.debug("BookAppointment: " + str(self.end_time))
        if self.start_time > self.end_time:
            frappe.throw("Start time cannot be greater than end time")
		# if start time - end time is greater than slot_size_in_mins then throw error
		slot_size_in_mins = frappe.get_value("Doctor", self.doctor, "slot_size_in_mins")
		if (self.end_time - self.start_time).total_seconds() > slot_size_in_mins * 60:
			frappe.throw("End time cannot be greater than start time + slot size")
		# fetch day from datetime_xqkn
		day = self.start_time.strftime("%A")
		# fetch availability from availability_xqkn
		availability = frappe.get_value("Availability", {"doctor": self.doctor, "day": day}, "name")
		if not availability:
			frappe.throw("Availability not found for this doctor and day")
		# check if start time is between start time and end time
		if self.start_time < availability.start_time or self.start_time > availability.end_time:
			frappe.throw("Start time is not between availability start time and end time")
		# check if end time is between start time and end time
		if self.end_time < availability.start_time or self.end_time > availability.end_time:
			frappe.throw("End time is not between availability start time and end time")

		# check for same doctor no other appointment at same date and time
		appointment = frappe.get_all("Book Appointment", {"doctor": self.doctor, "start_time": ["between", [self.start_time, self.end_time]]})
		if appointment:
			frappe.throw("Doctor is not available at this time")	

def has_permission(doc, ptype, user):
	# frappe.throw(user)
	logger.debug("User: " + user)
	if "System Manager" in frappe.get_roles(user):
		return True
	doctor_user = frappe.get_value("Doctor", doc.doctor, "email")
	logger.debug("Doctor User: " + doctor_user)
	if doctor_user == user:
		return True
	patient_user = frappe.get_value("Patient", doc.patient, "user_id")
	logger.debug("Patient User: " + patient_user)
	if patient_user == user:
		return True
	return False

def get_permission_query_conditions(user):
	logger.debug("User: " + user)
	if "System Manager" in frappe.get_roles(user):
		return ""	
	doctor = frappe.get_value("Doctor", {"email": user}, "name")
	logger.debug("Doctor: " + doctor)	
	patient = frappe.get_value("Patient", {"user_id": user}, "name")
	logger.debug("Patient: " + patient)	
	conditions = []
	if doctor:
		conditions.append(f"`tabBook Appointment`.doctor = '{doctor}'")
	if patient:
		conditions.append(f"`tabBook Appointment`.patient = '{patient}'")	
	if not conditions:
		return "1=0"  # no access	
	logger.debug("Conditions: " + str(conditions))
	return " OR ".join(conditions)
