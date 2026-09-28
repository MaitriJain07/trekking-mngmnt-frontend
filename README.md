# Safarnama — Trekking Management Application

## Setup Instructions

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Create `.env` file with: `SECRET_KEY=your-secret-key`
6. Seed the database: `python seed.py`
7. Run the app: `python run.py`
8. Visit: `http://127.0.0.1:5000`

## Default Admin Credentials
Email: admin@trekking.com
Password: admin123

## Tech Stack
Flask, SQLite, SQLAlchemy, Jinja2, HTML, CSS, and a small amount of vanilla JavaScript.

## Frontend
The responsive interface uses the original teal, ice, sage, and off-white palette. Shared styles live in `app/static/css/`, the local mountain artwork is in `app/static/images/`, and the mobile menu script is in `app/static/js/`. The page layouts and forms remain in `app/templates/`.
