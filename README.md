# MediQueue – Healthcare Appointment System

## 🩺 Project Overview

**MediQueue** is a Healthcare Appointment Management System built on the Frappe Framework with ERPNext and the Healthcare module. It enables small clinics, individual practitioners, or demo environments to manage doctor availability, book patient appointments, and streamline the healthcare workflow.

---

## 🚀 Key Features

- Role-based access for Patients, Doctors, and Admins.
- Custom Doctypes for Doctors, Appointments, and Availability.
- Patients can view doctors and book available slots.
- Doctors can manage availability and update appointment statuses.
- Admin dashboard with appointment stats, user management, and reports.
- Medicine Management & Prescriptions.

---

## 📦 Requirements
- Frappe Framework (Docker setup : https://github.com/frappe/frappe_docker)
- ERPNext
- Healthcare Module (https://github.com/earthians/marley version-15)
- MediQueue Module (https://github.com/krupalvora/mediqueue)

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/krupalvora/mediqueue --branch main
bench install-app mediqueue
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/mediqueue
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
