
from flask import Flask, render_template, request, jsonify, session, redirect
import pyodbc
import json
from datetime import datetime
import traceback

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Replace with actual DB info
conn_str = 'Driver={ODBC Driver 17 for SQL Server};Server=your_server;Database=your_db;UID=your_user;PWD=your_password'

@app.route('/')
def homepage():
    return "<h1>Welcome to the Mystery Shopper App</h1><p><a href='/shop-template-builder'>Build Template</a></p>"

@app.route('/dashboard')
def dashboard():
    return "<h2>Client Dashboard</h2><p>More features coming soon...</p>"

@app.route('/shop-template-builder')
def shop_template_builder():
    return render_template('Client_Shop_Template_Builder_FINAL_STYLE.html')

@app.route('/save-template', methods=['POST'])
def save_template():
    conn = None
    try:
        data = request.get_json()
        template_data = data.get('template')
        is_recommended_clicked = data.get('recommended', False)

        user_email = session.get('email', 'test@example.com')  # fallback for testing
        if not user_email:
            return jsonify({"error": "Not logged in"}), 401

        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        cursor.execute("SELECT client_id, company_name FROM clients WHERE LOWER(email) = ?", user_email.lower())
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Client not found"}), 404

        client_id, company_name = row
        recommended_name = f"{company_name}Recommended Template"

        selected_questions = 0
        has_custom = False
        for section, questions in template_data.items():
            for question in questions:
                if "custom" in question.lower() or "?" in question:
                    has_custom = True
                selected_questions += 1

        RECOMMENDED_COUNT = 100
        matches_recommended_structure = not has_custom and selected_questions == RECOMMENDED_COUNT

        cursor.execute("SELECT 1 FROM templates WHERE client_id = ? AND template_name = ?", client_id, recommended_name)
        already_exists = cursor.fetchone()

        if matches_recommended_structure and already_exists:
            return jsonify({"error": "You already have a Recommended Template saved. You cannot save another using the same structure."}), 409

        if matches_recommended_structure and not already_exists:
            template_name = recommended_name
        else:
            cursor.execute("SELECT COUNT(*) FROM templates WHERE client_id = ?", client_id)
            count = cursor.fetchone()[0] + 1
            template_name = f"{company_name}{count}"

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

if __name__ == "__main__":
    app.run(debug=True)
