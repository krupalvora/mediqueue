# Copyright (c) 2025, Krupalvora and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, get_time
from frappe.utils import logger
frappe.utils.logger.set_log_level("DEBUG")
logger = frappe.logger("BookAppointment", allow_site=True)

class BookAppointment(Document):
	def before_insert(self):
		self.status='Appointment Created'
		start_time = get_time(self.start_time)
		end_time = get_time(self.end_time)        
		if start_time > end_time:
			frappe.throw("Start time cannot be greater than end time.")        
		# Get slot size in minutes from Doctor doctype
		slot_size_in_mins = frappe.get_value("Doctor", self.doctor, "slot_size_in_mins")
		if not slot_size_in_mins:
			frappe.throw(f"Doctor {self.doctor} has no slot size defined.")        
		# Check if time difference exceeds slot size
		time_diff_minutes = (end_time.hour * 60 + end_time.minute) - (start_time.hour * 60 + start_time.minute)
		if time_diff_minutes > slot_size_in_mins:
			frappe.throw(f"Doctor slot size is {slot_size_in_mins} minutes. Please shorten the appointment duration.")        
			# Get day name like 'Monday'
		day = frappe.utils.get_datetime(self.start_time).strftime("%A")        
		# Get doctor's availability for that day
		doctor = frappe.get_doc("Doctor", self.doctor)
		matching_availability = None
		for row in doctor.slots:
			if row.day == day:
				matching_availability = row
				break        
		if not matching_availability:
			frappe.throw(f"Doctor {self.doctor} is not available on {day}.")
		available_start_time = get_time(str(matching_availability.start_time))
		available_end_time = get_time(str(matching_availability.end_time))
       
		if start_time < available_start_time or end_time > available_end_time:
			frappe.throw(
				f"Appointment time must be between {available_start_time} and {available_end_time} on {day}."
			)
		overlapping_appointments = frappe.get_all("Book Appointment",filters={"doctor": self.doctor, "start_time": ["<", end_time], "end_time": [">", start_time] },fields=["name"])
		if overlapping_appointments:
			frappe.throw("Doctor already has an appointment during this time. Please choose another slot.")


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
	logger.debug("User: " + str(user))
	if "System Manager" in frappe.get_roles(user):
		return ""	
	doctor = frappe.get_value("Doctor", {"email": user}, "name")
	logger.debug("Doctor: " + str(doctor))	
	patient = frappe.get_value("Patient", {"user_id": user}, "name")
	conditions = []
	if doctor:
		conditions.append(f"`tabBook Appointment`.doctor = '{doctor}'")
	if patient:
		conditions.append(f"`tabBook Appointment`.patient = '{patient}'")	
	if not conditions:
		return "1=0"  # no access	
	logger.debug("Conditions: " + str(conditions))
	return " OR ".join(conditions)
