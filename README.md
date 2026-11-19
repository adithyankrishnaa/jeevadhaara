# Jeevadhaara - Blood Donor Management System

A full-stack Python Django web application for managing voluntary blood donors, donor registration, multi-criteria search and filtering, and emergency blood access across the 14 districts of Kerala.

---

## Key Features

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

4. **Interactive Single Page Application (`/app/` or `index.html`)**:
   - Client-side interactive interface with instant view transitions between Home, Register, and Donors.
   - REST API integration with `/api/donors/` and `/api/register/` to persist registrations in SQLite.
   - Configurable backend URL connection via `.env` (`BACKEND_URL`).

5. **REST API Endpoints**:
   - `GET /api/donors/?district=<name>`: Returns registered donors in JSON format.
   - `POST /api/register/`: Accepts donor registrations and commits them to SQLite.

6. **MongoDB Atlas Cloud Synchronization (`save_to_mongodb.py`)**:
   - Export and synchronize all registered donors to MongoDB Atlas cluster (`jeevadhaara.tzdqdn0.mongodb.net`).
   - Upsert mechanism matching by ID and email to prevent duplication.
   - Automated index creation on `blood_group`, `city`, and `is_available`.
   - Run via standalone script: `python save_to_mongodb.py` or Django management command: `python manage.py save_to_mongodb`.

7. **Environment Variable Configuration (`.env`)**:
   - Configuration powered by `python-dotenv`:
     - `SECRET_KEY`: Django secret key
     - `DEBUG`: Debug mode toggle
     - `ALLOWED_HOSTS`: Allowed HTTP hosts
     - `BACKEND_URL`: URL of the backend API for client-side integration
     - `MONGODB_URI`: MongoDB Atlas connection URI

8. **Django Administration Back-Office (`/admin/`)**:
   - Model registration with `list_display`, `list_filter`, `search_fields`, and `list_editable`.
   - In-place toggling of donor availability directly from the admin table.
   - Role-based permissions, cryptographic password hashing (PBKDF2 SHA-256), and session auditing.

9. **Automated Unit & Integration Test Suite**:
   - Complete test suite in `donors/tests.py` with 16 automated tests passing at 100%.

---

## Project Structure

```text
jeevadhaara_django/
|-- manage.py
|-- requirements.txt
|-- README.md
|-- .env
|-- .env.example
|-- .gitignore
|-- db.sqlite3
|-- index.html
|-- save_to_mongodb.py
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
|           |-- seed_demo_data.py
|           \-- save_to_mongodb.py
\-- templates/
    \-- donors/
        |-- base.html
        |-- home.html
        |-- register.html
        |-- donor_list.html
        \-- app.html
```

---

## Quick Start Guide

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Contents of `.env`:
```env
SECRET_KEY=django-insecure-jeevadhaara-blood-donor-mgmt-key-2026-bca
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,*
BACKEND_URL=http://127.0.0.1:8000
MONGODB_URI=mongodb+srv://krishnaadithyan599_db_user:<db_password>@jeevadhaara.tzdqdn0.mongodb.net/?retryWrites=true&w=majority&appName=jeevadhaara
```

### 3. Apply Database Migrations
```bash
python manage.py migrate
```

### 4. Seed Demo Data & Superuser Credentials
```bash
python manage.py seed_demo_data
```

> **Default Admin Credentials**:
> - **Username**: `admin`
> - **Password**: `admin123`
> - **Admin URL**: `http://127.0.0.1:8000/admin/`

### 5. Run Development Server
```bash
python manage.py runserver
```

Open your browser and navigate to:
- **Home Page**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Register Donor**: [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/)
- **Find Donors**: [http://127.0.0.1:8000/donors/](http://127.0.0.1:8000/donors/)
- **Interactive App (SPA)**: [http://127.0.0.1:8000/app/](http://127.0.0.1:8000/app/)
- **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🍃 Exporting Data to MongoDB Atlas

To export and synchronize all donor records to your MongoDB Atlas cluster:

### Option A: Using the Standalone Python Script
```bash
python save_to_mongodb.py --password YOUR_ATLAS_PASSWORD
```
Or interactively (will prompt for password securely):
```bash
python save_to_mongodb.py
```

### Option B: Using the Django Management Command
```bash
python manage.py save_to_mongodb --password YOUR_ATLAS_PASSWORD
```

Target Cluster: `jeevadhaara.tzdqdn0.mongodb.net`  
Database: `jeevadhaara`  
Collection: `donors`  

---

## Running Automated Tests

Run the test suite to verify all 16 tests:

```bash
python manage.py test donors
```

---

## Academic Internship Report

The complete, formatted academic internship project report conforming to Bengaluru North University guidelines is available in the repository:
- **Report Document**: [docs/Jeevadhaara_Final_Formatted_Report.pdf](docs/Jeevadhaara_Final_Formatted_Report.pdf) (32 Pages, Formatted with TOC, Architecture, and Outcomes)
