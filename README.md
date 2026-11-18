# Jeevadhaara - Blood Donor Management System

A full-stack Python Django web application for managing voluntary blood donors, donor registration, multi-criteria search and filtering, and emergency blood access across the 14 districts of Kerala.

---

## 🩸 Features

1. **Modern Hero Landing Page (`/`)**:
   - Modern medical hero banner with Kerala blood bank theme (`#DC2626`).
   - Bilingual brand styling: **Jeevadhaara** (`ജീവാധാര കേരള ബ്ലഡ് ബാങ്ക്`).
   - Real-time statistics counters (Registered Donors, Available Donors, Blood Groups).
   - Interactive blood group inventory cards for all 8 ABO/Rh types (A+, A-, B+, B-, AB+, AB-, O+, O-).
   - Direct call-to-action buttons for donor registration and directory lookup.

2. **Donor Registration Portal (`/register/`)**:
   - Comprehensive registration form powered by Django `ModelForm`.
   - Fields: Full Name, Blood Group (ABO/Rh), Contact Number (with regex validation), Kerala District, Local Area, Availability status.
   - Robust server-side input validation, error handling, and animated success messages via Django's `messages` framework.
   - Built-in CSRF protection against cross-site request forgery.

3. **Donor Directory & Search Engine (`/donors/`)**:
   - Tabular directory with responsive layout and horizontal mobile scrolling.
   - Colorful, high-contrast badges for each blood group.
   - Multi-parameter filtering: filter by Kerala district, blood group, or availability.
   - Full-text search across donor names, districts, and local area keywords using Django `Q` objects.
   - One-click contact action buttons (`tel:` link).
   - Informative empty-state guidance when search criteria yield zero matches.

4. **Django Administration Back-Office (`/admin/`)**:
   - Model registration with `list_display`, `list_filter`, `search_fields`, and `list_editable`.
   - In-place toggling of donor availability directly from the admin table.
   - Role-based permissions, cryptographic password hashing (PBKDF2 SHA-256), and session auditing.

5. **Realistic Demo Data Seeding**:
   - Custom Django management command `python manage.py seed_demo_data` populating realistic sample records across Kerala districts and creating default superuser credentials.

6. **Automated Unit & Integration Test Suite**:
   - Complete test suite in `donors/tests.py` validating models, forms, QuerySet filtering, and HTTP views with 100% pass rate.

---

## 📁 Project Structure

```text
jeevadhaara_django/
|-- manage.py
|-- requirements.txt
|-- README.md
|-- db.sqlite3
|-- docs/
|   \-- Jeevadhaara_Final_Formatted_Report.pdf
|-- jeevadhaara/
|   |-- __init__.py
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   \-- wsgi.py
|-- donors/
|   |-- __init__.py
|   |-- models.py
|   |-- forms.py
|   |-- views.py
|   |-- urls.py
|   |-- admin.py
|   |-- tests.py
|   |-- migrations/
|   |   |-- __init__.py
|   |   \-- 0001_initial.py
|   \-- management/
|       |-- __init__.py
|       \-- commands/
|           |-- __init__.py
|           \-- seed_demo_data.py
\-- templates/
    \-- donors/
        |-- base.html
        |-- home.html
        |-- register.html
        \-- donor_list.html
```

---

## 📄 Academic Internship Report

The complete, formatted academic internship project report conforming to Bengaluru North University guidelines is available in the repository:
- **Report Document**: [docs/Jeevadhaara_Final_Formatted_Report.pdf](docs/Jeevadhaara_Final_Formatted_Report.pdf) (32 Pages, Formatted with TOC, Architecture, and Outcomes)

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Apply Database Migrations
```bash
python manage.py migrate
```

### 3. Seed Demo Data & Superuser Credentials
```bash
python manage.py seed_demo_data
```

> **Default Admin Credentials**:
> - **Username**: `admin`
> - **Password**: `admin123`
> - **Admin URL**: `http://127.0.0.1:8000/admin/`

### 4. Run Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Home Page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Register Donor**: [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/)
- **Find Donors**: [http://127.0.0.1:8000/donors/](http://127.0.0.1:8000/donors/)
- **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🧪 Running Automated Tests

Run the test suite to verify all 13 tests:

```bash
python manage.py test donors
```
