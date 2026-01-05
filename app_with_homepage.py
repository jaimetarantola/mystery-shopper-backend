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

# =========================
# SQL Server Configuration
# =========================
server = 'DESKTOP-GANGRVA'
database = 'mystery_shopper'

conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes;'
)

# =========================
# Home & Pages
# =========================
@app.route('/')
def home():
    return render_template('Client Homepage.html')

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
    return render_template('client_dashboard_mockup.html',
                           company_name=session.get('company_name'))

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

# =========================
# Auth Routes
# =========================
@app.route('/register', methods=['POST'])
def register():
    conn = None
    try:
        data = request.get_json()
        email = data['email'].strip().lower()

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM clients WHERE LOWER(email) = ?", email)
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
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['company_name'], data['company_address'], data['company_city'],
            data['company_state'], data['company_zip'],
            data['client_first_name'], data['client_last_name'],
            email, data['client_phone'], hashed_password
        ))

        conn.commit()
        return jsonify({"message": "Client registered successfully"}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/login', methods=['POST'])
def login():
    conn = None
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password_hash, company_name FROM clients WHERE LOWER(email) = ?",
            email
        )
        row = cursor.fetchone()

        if not row or not check_password_hash(row[0], password):
            return jsonify({"error": "Invalid email or password"}), 401

        session['email'] = email
        session['company_name'] = row[1]

        return jsonify({"message": "Login successful"}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

# =========================
# Template Routes
# =========================
@app.route('/save-template', methods=['POST'])
def save_template():
    conn = None
    try:
        data = request.get_json()
        template_data = data.get('template')
        is_recommended = data.get('recommended', False)
        template_id = data.get('template_id')

        user_email = session.get('email')
        if not user_email:
            return jsonify({"error": "Not logged in"}), 401

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT client_id, company_name
            FROM clients
            WHERE LOWER(email) = ?
        """, user_email.lower())

        client = cursor.fetchone()
        if not client:
            return jsonify({"error": "Client not found"}), 404

        client_id, company_name = client
        template_json = json.dumps(template_data)

        if template_id:
            cursor.execute("""
                UPDATE templates
                SET template_data = ?, created_at = ?
                WHERE template_id = ? AND client_id = ?
            """, (template_json, datetime.now(), template_id, client_id))
            conn.commit()
            return jsonify({"message": "Template updated."}), 200

        if is_recommended:
            template_name = "Recommended"
            cursor.execute("""
                SELECT 1 FROM templates
                WHERE client_id = ? AND template_name = ?
            """, client_id, template_name)
            if cursor.fetchone():
                return jsonify({"error": "Recommended template already exists"}), 409
        else:
            cursor.execute(
                "SELECT COUNT(*) FROM templates WHERE client_id = ?",
                client_id
            )
            count = cursor.fetchone()[0] + 1
            template_name = f"{company_name}{count}"

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

@app.route('/api/client-templates')
def get_client_templates():
    conn = None
    try:
        user_email = session.get('email')
        if not user_email:
            return jsonify([])

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT t.template_id, t.template_name, t.created_at
            FROM templates t
            JOIN clients c ON t.client_id = c.client_id
            WHERE LOWER(c.email) = ?
            ORDER BY t.created_at DESC
        """, user_email.lower())

        rows = cursor.fetchall()

        return jsonify([
            {
                "template_id": r[0],
                "template_name": r[1],
                "created_at": r[2].isoformat()
            } for r in rows
        ])

    except Exception:
        traceback.print_exc()
        return jsonify([])
    finally:
        if conn:
            conn.close()

@app.route('/template/<int:template_id>')
def view_template(template_id):
    conn = None
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT template_name, template_data
            FROM templates
            WHERE template_id = ?
        """, template_id)

        row = cursor.fetchone()
        if not row:
            return "Template not found", 404

        return render_template(
            'view_template.html',
            template_name=row[0],
            template_data=json.loads(row[1])
        )

    except Exception:
        traceback.print_exc()
        return "Error loading template", 500
    finally:
        if conn:
            conn.close()

@app.route('/edit-template/<int:template_id>')
def edit_template(template_id):
    if 'email' not in session:
        return redirect(url_for('login_page'))

    conn = None
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT template_name, template_data
            FROM templates
            WHERE template_id = ?
        """, template_id)

        row = cursor.fetchone()
        if not row:
            return "Template not found", 404

        return render_template(
            'Client Shop Template Builder.html',
            template_id=template_id,
            template_name=row[0],
            template_data=json.loads(row[1])
        )

    except Exception:
        traceback.print_exc()
        return "Error loading template", 500
    finally:
        if conn:
            conn.close()

@app.route('/delete-template/<int:template_id>', methods=['POST'])
def delete_template(template_id):
    conn = None
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM template_questions WHERE template_id = ?", template_id)
        cursor.execute("DELETE FROM templates WHERE template_id = ?", template_id)
        conn.commit()

        return '', 204

    except Exception:
        traceback.print_exc()
        return "Error deleting template", 500
    finally:
        if conn:
            conn.close()

@app.route('/rename-template/<int:template_id>', methods=['POST'])
def rename_template(template_id):
    conn = None
    try:
        data = request.get_json()
        new_name = data.get('new_name', '').strip()

        if not new_name:
            return jsonify({"error": "New name required"}), 400

        user_email = session.get('email')
        if not user_email:
            return jsonify({"error": "Not logged in"}), 401

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT client_id FROM clients WHERE LOWER(email) = ?
        """, user_email.lower())
        client_id = cursor.fetchone()[0]

        cursor.execute("""
            SELECT 1 FROM templates
            WHERE client_id = ? AND template_name = ? AND template_id != ?
        """, (client_id, new_name, template_id))

        if cursor.fetchone():
            return jsonify({"error": "Template name already exists"}), 409

        cursor.execute("""
            UPDATE templates SET template_name = ?
            WHERE template_id = ?
        """, (new_name, template_id))

        conn.commit()
        return '', 204

    except Exception:
        traceback.print_exc()
        return jsonify({"error": "Rename failed"}), 500
    finally:
        if conn:
            conn.close()

# =========================
# Run App
# =========================
if __name__ == '__main__':
    app.run(debug=True)
