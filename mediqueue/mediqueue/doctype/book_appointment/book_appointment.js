frappe.ui.form.on('Book Appointment', {
    onload: function(frm) {
        console.log("User -------------- Roles: " + frappe.user_roles);
        if (frappe.user_roles.includes("Patient")) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Patient",
                    filters: {
                        email: frappe.session.user
                    },
                    fields: ["name"]
                },
                callback: function(r) {
                    if (r.message && r.message.length > 0) {
                        const patient_name = r.message[0].name;

                        // Set patient field if not already set
                        if (!frm.doc.patient) {
                            frm.set_value("patient", patient_name);
                        }

                        // Set dropdown query to only that patient
                        frm.set_query("patient", function() {
                            return {
                                filters: {
                                    name: patient_name
                                }
                            };
                        });

                        // Disable the field for patient role
                        frm.set_df_property("patient", "read_only", 1);
                    }
                }
            });
        }
    }
});
