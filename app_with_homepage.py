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

server = 'DESKTOP-GANGRVA'
database = 'mystery_shopper'
conn_str = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    f'SERVER={server};'
    f'DATABASE={database};'
    'Trusted_Connection=yes;'
)

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

@app.route('/save-template', methods=['POST'])
def save_template():
    conn = None
    try:
        data = request.get_json()
        user_email = session.get('email')
        if not user_email:
            return jsonify({"error": "Not logged in"}), 401

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Get client_id and company_name
        cursor.execute("SELECT client_id, company_name FROM clients WHERE LOWER(email) = ?", user_email.lower())
        client = cursor.fetchone()
        if not client:
            return jsonify({"error": "Client not found"}), 404

        client_id, company_name = client

        # Count existing templates for naming
        cursor.execute("SELECT COUNT(*) FROM templates WHERE client_id = ?", client_id)
        template_count = cursor.fetchone()[0] + 1
        template_name = f"{company_name}{template_count}"

        # Save JSON string of the template data
        template_json = json.dumps(data)

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




