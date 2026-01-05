🕵️ Mystery Shopper Web App
This is a Flask-based web application that allows clients to register, log in, and build custom mystery shop templates for use in evaluations.

🔧 Features
✅ Client Registration & Authentication
Clients can create an account with company and contact information
- Email uniqueness enforced — duplicates are rejected with a warning
- Passwords securely hashed using werkzeug.security
- Login and Logout functionality using Flask sessions
- After login, clients are taken to their Dashboard

🖥️ Client Dashboard
After successful login, clients can:
- View a personalized welcome message
- Navigate using the sidebar:
  - Edit Profile (coming soon)
  - Shop Templates – opens a new shop templates page

🧾 Shop Templates Workflow
From the dashboard:
- Clicking “Shop Templates” routes to `/shop-templates`
- Clients see:
  - Build a New Shop Template → links to `/shop-template-builder`
  - View Your Shop Templates → placeholder for future viewing functionality

✏️ Shop Template Builder
The `/shop-template-builder` route opens the template creation form
Clients can:
- Choose evaluation questions (checkboxes grouped by section)
- Add custom questions per section
- Organize them into reusable templates saved in SQL

📥 Template Saving Behavior
- Data from the form is sent as JSON
- Backend saves template into two tables:
  1. `templates` – includes client ID, template name, full JSON data
  2. `template_questions` – includes all possible questions with:
     - Section name
     - Question text
     - Flags for `is_custom` and `is_selected`

🧠 Recommended Template Logic
Clients can toggle a “Use Recommended Template” checkbox at the top of the form:
✅ If selected:
- All standard questions are automatically checked
- If saved without changes:
  - Template is stored as **"Recommended"** (one per client)
  - Any duplicate save attempt is blocked with an error

🛠️ If the client unchecks a box or adds a custom question:
- The `recommended` toggle unchecks automatically via JavaScript
- The template is saved with a dynamic name: `Company1`, `Company2`, etc.

🗂️ Folder Structure
/project-root
│
├── app_with_homepage.py            # Flask app logic and routes
├── /templates
│   ├── Client Homepage.html
│   ├── Client Login.html
│   ├── Client_Account.html
│   ├── client_dashboard_mockup.html
│   ├── Client Shop Template Builder.html
│   └── shop_templates_home.html
│
└── README_FINAL_UPDATED.md

🚀 Running the App
1. Start the Flask App
```bash
python app_with_homepage.py
```
2. Access via Browser
```url
http://127.0.0.1:5000/
```

✅ SQL Setup (Required Tables)
```sql
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

CREATE TABLE templates (
  template_id INT IDENTITY(1,1) PRIMARY KEY,
  client_id INT FOREIGN KEY REFERENCES clients(client_id),
  template_name VARCHAR(100),
  template_data TEXT,
  created_at DATETIME
);

CREATE TABLE template_questions (
  question_id INT IDENTITY(1,1) PRIMARY KEY,
  template_id INT FOREIGN KEY REFERENCES templates(template_id),
  section_name VARCHAR(100),
  question_text TEXT,
  is_custom BIT,
  is_selected BIT,
  created_at DATETIME DEFAULT GETDATE()
);
```

Let me know if you'd like to add SQL scripts, GitHub setup steps, or deployment instructions.
