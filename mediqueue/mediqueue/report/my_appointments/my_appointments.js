// Copyright (c) 2025, Krupalvora and contributors
// For license information, please see license.txt

frappe.query_reports["My Appointments"] = {
	"filters": [
		{
			"fieldname": "status",
			"label": "Status",
			"fieldtype": "Select",
			"options": "\nAppointment Created\nAppointment Accepted\nCompleted\nRejected\nNo-show",
			"default": "",
			"reqd": 0
		},
		{
			"fieldname": "from_date",
			"label": "From Date",
			"fieldtype": "Date"
		},
		{
			"fieldname": "to_date",
			"label": "To Date",
			"fieldtype": "Date"
		}
	]
};
