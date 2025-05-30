# Copyright (c) 2025, Krupalvora and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class Doctor(Document):
    def after_insert(self):
        self.create_website_user()

    def create_website_user(self):
        if not self.email:
            return        
        # Check if user already exists
        if frappe.db.exists("User", self.email):
            return  # Skip creation if user exists        
        # Proceed to create new user
        user = frappe.get_doc({
            "doctype": "User",
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "user_type": "Website User",
            "phone": self.mobile,
            "mobile_no": self.mobile
        })
        user.flags.ignore_permissions = True
        user.enabled = True
        user.send_welcome_email = True
        user.add_roles("Doctor")
        user.add_roles("Appointment")
        user.insert()
