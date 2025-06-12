from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import pyodbc
import traceback
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey123'
CORS(app)

# SQL Server config
server = 'DESKTOP-GANGRVA'
database = 'mystery_shopper'
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes;'
)

# Home
@app.route('/')
def home():
    return render_template('Client Homepage.html')

# Pages
@app.route('/register-page')
def register_page():
    return render_template('Client_Account.html')

@app.route('/login-page')
def login_page():
    return render_template('Client Login.html')

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('home'))
    return render_template('client_dashboard_mockup.html', company_name=session.get('company_name'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/shop-templates')
def shop_templates():
    if 'email' not in session:
        return redirect(url_for('login_page'))
    return render_template('shop_templates_home.html')

@app.route('/shop-template-builder')
def shop_template_builder():
    if 'email' not in session:
        return redirect(url_for('login_page'))
    return render_template('Client Shop Template Builder.html')

# Register
@app.route('/register', methods=['POST'])
def register():
    conn = None
    try:
        data = request.get_json()
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        email = data['email'].strip().lower()
        cursor.execute("SELECT * FROM clients WHERE LOWER(email) = ?", email)
        if cursor.fetchone():
            return jsonify({"error": "Email already registered"}), 409

        password = data.get('password')
        if not password:
            return jsonify({"error": "Password is required"}), 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        cursor.execute("""
            INSERT INTO clients (
                company_name, company_address, company_city, company_state, company_zip,
                client_first_name, client_last_name, email, client_phone, password_hash
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['company_name'], data['company_address'], data['company_city'], data['company_state'], data['company_zip'],
            data['client_first_name'], data['client_last_name'], email, data['client_phone'], hashed_password
        ))

        conn.commit()
        return jsonify({"message": "Client registered successfully"}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

# ✅ Login restored
@app.route('/login', methods=['POST'])
def login():
    conn = None
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash, company_name FROM clients WHERE LOWER(email) = ?", email)
        row = cursor.fetchone()

        if not row:
            return jsonify({"error": "Invalid email or password"}), 401

        hashed_password, company_name = row
        if not check_password_hash(hashed_password, password):
            return jsonify({"error": "Invalid email or password"}), 401

        session['email'] = email
        session['company_name'] = company_name

        return jsonify({"message": "Login successful", "company_name": company_name}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

# ✅ Save template
@app.route('/save-template', methods=['POST'])
def save_template():
    conn = None
    try:
        data = request.get_json()
        template_data = data.get('template')
        is_recommended_clicked = data.get('recommended', False)

        user_email = session.get('email')
        if not user_email:
            return jsonify({"error": "Not logged in"}), 401

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Get client info
        cursor.execute("SELECT client_id, company_name FROM clients WHERE LOWER(email) = ?", user_email.lower())
        client = cursor.fetchone()
        if not client:
            return jsonify({"error": "Client not found"}), 404

        client_id, company_name = client

        # Analyze submission
        selected_questions = 0
        has_custom = False

        for section, questions in template_data.items():
            for question in questions:
                q_lower = question.lower()
                if 'custom' in q_lower or '?' in question:
                    has_custom = True
                selected_questions += 1

        # Reference config for recommended template match
        EXACT_RECOMMENDED_COUNT = 100
        is_exact_recommended_structure = not has_custom and selected_questions == EXACT_RECOMMENDED_COUNT
        recommended_name = f"{company_name}Recommended Template"

        # Check for existing recommended template
        cursor.execute("SELECT COUNT(*) FROM templates WHERE client_id = ? AND template_name = ?", client_id, recommended_name)
        has_recommended_template = cursor.fetchone()[0] > 0

        # ❌ ABSOLUTE BLOCK: if submitted structure matches recommended AND one already exists
        if is_exact_recommended_structure and has_recommended_template:
            return jsonify({"error": "You already have a Recommended Template saved. This exact structure cannot be saved again."}), 409

        # ✅ Save as recommended (first time only)
        if is_recommended_clicked and is_exact_recommended_structure and not has_recommended_template:
            template_name = recommended_name
        else:
            # ✅ Save as custom
            cursor.execute("SELECT COUNT(*) FROM templates WHERE client_id = ?", client_id)
            template_count = cursor.fetchone()[0] + 1
            template_name = f"{company_name}{template_count}"

        # Save the template
        template_json = json.dumps(template_data)
        cursor.execute("""
            INSERT INTO templates (client_id, template_name, template_data, created_at)
            VALUES (?, ?, ?, ?)
        """, (client_id, template_name, template_json, datetime.now()))
        conn.commit()
        return jsonify({"message": f"Template '{template_name}' saved!"}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)

