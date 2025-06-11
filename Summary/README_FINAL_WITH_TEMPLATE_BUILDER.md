🕵️ Mystery Shopper Web App
This is a Flask-based web application that allows clients to register, log in, and build custom mystery shop templates for use in evaluations.

🔧 Features
✅ Client Registration & Authentication
Clients can create an account with company and contact information

Email uniqueness enforced — duplicates are rejected with a warning

Passwords securely hashed using werkzeug.security

Login and Logout functionality using Flask sessions

After login, clients are taken to their Dashboard

🖥️ Client Dashboard
After successful login, clients can:

View a personalized welcome message

Navigate using the sidebar:

Edit Profile (coming soon)

Shop Templates – opens a new shop templates page

🧾 Shop Templates Workflow
From the dashboard:

Clicking “Shop Templates” routes to /shop-templates

Clients see:

Build a New Shop Template → links to /shop-template-builder

View Your Shop Templates → placeholder for future viewing functionality

✏️ Shop Template Builder
The /shop-template-builder route opens the template creation form

Clients can:

Choose evaluation questions

Add custom questions

Organize them into reusable templates

🗂️ Folder Structure
arduino
Copy
Edit
/project-root
│
├── app_with_homepage.py            # Flask app
├── /templates
│   ├── Client Homepage.html
│   ├── Client Login.html
│   ├── Client_Account.html
│   ├── client_dashboard_mockup.html
│   ├── Client Shop Template Builder.html
│   └── shop_templates_home.html
│
└── README_FINAL_WITH_TEMPLATE_BUILDER.md
🚀 Running the App
1. Start the Flask App
bash
Copy
Edit
python app_with_homepage.py
2. Access via Browser
Visit:

cpp
Copy
Edit
http://127.0.0.1:5000/
✅ SQL Setup (Example)
Ensure the clients table in SQL Server includes:

sql
Copy
Edit
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
Let me know if you want me to include SQL for shop templates or link this README to GitHub formatting!








