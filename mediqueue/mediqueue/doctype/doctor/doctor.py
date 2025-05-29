# Copyright (c) 2025, Krupalvora and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class Doctor(Document):
	def on_update(self):
		self.create_website_user()

	def create_website_user(self):
		users = frappe.db.get_all(
			"User",
			fields=["email"],
			or_filters={"email": self.email},
		)
		if users and users[0]:
			frappe.throw(
				_(
					"User exists with Email {}<br>Please check email or disable 'Invite as User' to skip creating User"
				).format(frappe.bold(users[0].email)),
				frappe.DuplicateEntryError,
			)

		user = frappe.get_doc(
			{
				"doctype": "User",
				"first_name": self.first_name,
				"last_name": self.last_name,
				"email": self.email,
				"user_type": "Website User",
				"phone": self.mobile,
				"mobile_no": self.mobile
			}
		)
		user.flags.ignore_permissions = True
		user.enabled = True
		user.send_welcome_email = True
		user.add_roles("Doctor")
		user.add_roles("Appointment")
		# self.db_set("user_id", user.name)
