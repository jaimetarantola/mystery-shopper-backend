from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import pyodbc
import traceback

app = Flask(__name__)
app.secret_key = 'supersecretkey123'  # Replace with a secure key in production
CORS(app)

# SQL Server connection string
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

@app.route('/test', methods=['GET'])
def test():
    return jsonify({"message": "Flask is running!"})

@app.route('/register', methods=['POST'])
def register():
    conn = None
    try:
        data = request.get_json()
        print("Received data:", data)

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        email = data['email'].strip().lower()
        cursor.execute("SELECT * FROM clients WHERE LOWER(email) = ?", email)
        if cursor.fetchone():
            return jsonify({"error": "Email already registered"}), 409

        password = data.get('password')
        if not password:
            return jsonify({"error": "Password is required"}), 400
        
        # FIX: use PBKDF2 explicitly to avoid 'scrypt' error
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

@app.route('/client-shop-template-builder')
def template_builder():
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/save-template', methods=['POST'])
def save_template():
    if 'email' not in session:
        return jsonify({"error": "You must be logged in"}), 401

    conn = None
    try:
        data = request.get_json()
        user_email = session['email']

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        # Get client_id and company_name
        cursor.execute("SELECT client_id, company_name FROM clients WHERE LOWER(email) = ?", user_email)
        client = cursor.fetchone()
        if not client:
            return jsonify({"error": "Client not found"}), 404

        client_id, company_name = client

        # Count how many templates this client already has
        cursor.execute("SELECT COUNT(*) FROM templates WHERE client_id = ?", client_id)
        count = cursor.fetchone()[0]

        template_name = f"{company_name}{count + 1}"

        cursor.execute("""
            INSERT INTO templates (client_id, template_name, template_data, created_at)
            VALUES (?, ?, ?, GETDATE())
        """, (client_id, template_name, str(data)))

        conn.commit()
        return jsonify({"message": f"Template '{template_name}' saved!"}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

