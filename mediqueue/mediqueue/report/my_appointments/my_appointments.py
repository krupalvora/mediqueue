import frappe

def execute(filters=None):
    user = frappe.session.user
    roles = frappe.get_roles(user)
    print(user,roles,'---------------------------------------')
    columns = [
        {"label": "Appointment ID", "fieldname": "name", "fieldtype": "Link", "options": "Book Appointment", "width": 150},
        {"label": "Doctor", "fieldname": "doctor", "fieldtype": "Link", "options": "Healthcare Practitioner", "width": 150},
        {"label": "Patient", "fieldname": "patient", "fieldtype": "Link", "options": "Patient", "width": 150},
        {"label": "Status", "fieldname": "status", "fieldtype": "Data", "width": 120},
        {"label": "Appointment Date", "fieldname": "datetime_xqkn", "fieldtype": "Date", "width": 120},
        {"label": "Last Updated", "fieldname": "modified", "fieldtype": "Datetime", "width": 160},
    ]

    conditions = "1=1"
    params = {}
    if "Administrator" in roles or "System Manager" in roles:
        # Full access
        pass
    elif "Doctor" in roles:
        print('------------------------here-----------')
		#this user is same as logged in user we will have to fetch it from name from doctor where email = user
        doctor = frappe.get_value("Doctor", {"email": user}, "name")
        print(doctor,'doctor')
        conditions += " AND doctor = %(doctor)s"
        params["doctor"] = doctor
    elif "Patient" in roles:
		#this user is same as logged in user we will have to fetch it from name from patient where user_id = user
        patient = frappe.get_value("Patient", {"user_id": user}, "name")
        conditions += " AND patient = %(patient)s"
        params["patient"] = patient
    else:
        frappe.throw("You are not authorized to view this report.")

    print(conditions,'conditions',params,'params')
    if filters:
        if filters.get("status"):
            conditions += " AND status = %(status)s"
            params["status"] = filters["status"]

        if filters.get("from_date"):
            conditions += " AND datetime_xqkn >= %(from_date)s"
            params["from_date"] = filters["from_date"]

        if filters.get("to_date"):
            conditions += " AND datetime_xqkn <= %(to_date)s"
            params["to_date"] = filters["to_date"]

    print(conditions,'conditions')
    print(params,'params')
    data = frappe.db.sql(f"""
        SELECT
            name, doctor, patient, status, datetime_xqkn, modified
        FROM
            `tabBook Appointment`
        WHERE
            {conditions}
        ORDER BY
            datetime_xqkn ASC
    """, params, as_dict=True)
    print(data,'data')
    # print(data,'data')
    return columns, data
