# Jeevadhara - Blood Donor Management System

A full-stack Python Django web application for managing voluntary blood donors, donor registration, search and filtering, and emergency blood access.

---

## 🩸 Features

1. **Attractive Landing Page (`/`)**:
   - Modern medical hero banner with primary color `#C62828`.
   - Real-time statistics counters (Registered Donors, Available Donors, Blood Groups).
   - Donors count grouped across all 8 blood groups (A+, A-, B+, B-, AB+, AB-, O+, O-).
   - Blood donation awareness, medical benefits, and 4-step donation workflow.
   - Medical eligibility criteria checklist.
   - Emergency helpline integration.

2. **Donor Registration (`/register/`)**:
   - Comprehensive registration form powered by Django `ModelForm`.
   - Fields: Full Name, Email, Phone, Age (18–65), Gender, Blood Group, City, Address, Availability status.
   - Server-side input validation and custom age/name/city sanitization.
   - CSRF protection and animated alert messages.

3. **Donor Search & Filter Directory (`/donors/`)**:
   - Responsive donor cards with blood group circular badges.
   - Real-time search by city name, donor name, or address.
   - Dropdown filter by blood group.
   - Availability toggle filter (Available Only / Unavailable / All).
   - Quick city filter pills for one-click filtering.
   - Direct contact actions (Click-to-Call `tel:` and Click-to-Email `mailto:`).
   - User-friendly empty state when search criteria yield zero matches.

4. **Django Administration Portal (`/admin/`)**:
   - Model registration with `list_display`, `list_filter`, and `search_fields`.
   - Inline toggling of `is_available` status.
   - Date hierarchy navigation and customized administrative headers.
   - Custom admin bulk actions ("Mark selected donors as Available / Unavailable").

5. **Realistic Demo Data Seeding**:
   - `python manage.py seed_demo_data` command seeds 12 realistic donors across multiple cities and all 8 blood groups, plus creates a default superuser.

6. **Automated Unit & Integration Tests**:
   - Complete test suite in `donors/tests.py` covering models, forms, and views.

---

## 📁 Project Structure

```text
jeevadhaara_django/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3
├── jeevadhaara/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── donors/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   ├── tests.py
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py
│   └── management/
│       ├── __init__.py
│       └── commands/
│           ├── __init__.py
│           └── seed_demo_data.py
└── templates/
    └── donors/
        ├── base.html
        ├── home.html
        ├── register.html
        └── donor_list.html
```

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
Open your terminal in the `jeevadhaara_django` directory and install the required packages:

```bash
cd c:\Users\krish\OneDrive\Documents\internship\jeevadhaara_django
pip install -r requirements.txt
```

### 2. Apply Database Migrations
Create and configure the SQLite database:

```bash
python manage.py migrate
```

### 3. Seed Demo Data & Admin Superuser
Populate the database with sample donors and generate default administrator credentials:

```bash
python manage.py seed_demo_data
```

> **Default Admin Credentials**:
> - **Username**: `admin`
> - **Password**: `admin123`
> - **Admin URL**: `http://127.0.0.1:8000/admin/`

### 4. Run the Development Server

```bash
python manage.py runserver
```

Open your web browser and navigate to:
- **Home Page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Register Donor**: [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/)
- **Search & Filter Donors**: [http://127.0.0.1:8000/donors/](http://127.0.0.1:8000/donors/)
- **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Running Automated Tests

To execute the 13 automated unit and integration tests:

```bash
python manage.py test donors
```
