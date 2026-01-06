🕵️ Mystery Shopper Web App

This is a Flask-based web application that allows clients to register, log in, and build custom mystery shop templates for use in evaluations.

The application is designed to run locally for development and demonstration purposes. It is not deployed by default and does not need to be running continuously.

🔧 Features
✅ Client Registration & Authentication

Clients can create an account with company and contact information

Email uniqueness is enforced — duplicate registrations are rejected

Passwords are securely hashed using werkzeug.security

Login and logout functionality implemented using Flask sessions

After login, clients are routed to their dashboard

🖥️ Client Dashboard

After successful login, clients can:

View a personalized welcome message

Navigate using the sidebar:

Edit Profile (coming soon)

Shop Templates – opens the shop templates workflow

🧾 Shop Templates Workflow

From the dashboard:

Clicking Shop Templates routes to /shop-templates

Clients can:

Build a new shop template

View previously created templates (in progress)

Edit, rename, or delete templates

✏️ Shop Template Builder

The /shop-template-builder route opens the template creation interface.

Clients can:

Select evaluation questions

Add custom questions

Organize questions into reusable templates

Save templates to be reused across mystery shopping evaluations

🧠 How Flask Is Used (Important Note)

Flask acts as the local web server and application layer for this project.

Flask handles:

Routing

Session-based authentication

Form submission

Template rendering

Flask does not need to be running at all times

Recruiters or reviewers are not expected to have the app running live

The application is intended to be:

Run locally during development

Demonstrated via screenshots or walkthroughs

Reviewed primarily through code and documentation

🗂️ Folder Structure
/project-root
│
├── app_with_homepage.py            # Main Flask application
├── /Templates                      # Jinja2 HTML templates
│   ├── Client Homepage.html
│   ├── Client Login.html
│   ├── Client_Account.html
│   ├── client_dashboard_mockup.html
│   ├── Client Shop Template Builder.html
│   ├── shop_templates_home.html
│   └── view_template.html
│
├── /Summary                        # Project notes and documentation
└── README.md

🚀 Running the App Locally
1️⃣ Start the Flask application
python app_with_homepage.py

2️⃣ Access via browser

Visit:

http://127.0.0.1:5000/

🐍 Environment Notes

The project is typically run using:

A Python virtual environment or

A Conda environment (recommended on Windows)

Virtual environments are intentionally excluded from version control

Python dependencies are installed locally per environment

🔐 Security & Secrets

Sensitive values (e.g., tokens, credentials) are not committed

Secrets should be stored in:

Environment variables, or

.env files (excluded via .gitignore)

GitHub push protection is enabled to prevent accidental secret exposure

🗄️ SQL Setup (Example)

The application expects a SQL Server database with a clients table similar to:

CREATE TABLE clients (
    client_id INT IDENTITY(1,1) PRIMARY KEY,
    company_name VARCHAR(100),
    company_address TEXT,
    company_city VARCHAR(50),
    company_state VARCHAR(2),
    company_zip VARCHAR(10),
    client_first_name VARCHAR(50),
    client_last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    client_phone VARCHAR(20),
    password_hash TEXT
);


Additional tables (e.g., templates, template questions) support the shop template workflow.

📌 Project Status

Core client authentication and template-building workflows are implemented

Shopper-side submission and reporting workflows are planned but not yet complete

This project represents an in-progress MVP focused on extensibility and clarity