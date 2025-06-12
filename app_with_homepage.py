
from flask import Flask, request, jsonify, session
import pyodbc
import json
from datetime import datetime
import traceback

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Adjust your connection string as needed
conn_str = 'Driver={ODBC Driver 17 for SQL Server};Server=your_server;Database=your_db;UID=your_user;PWD=your_password'

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

        # Get client_id and company_name
        cursor.execute("SELECT client_id, company_name FROM clients WHERE LOWER(email) = ?", user_email.lower())
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Client not found"}), 404

        client_id, company_name = row
        recommended_name = f"{company_name}Recommended Template"

        # Count selected questions and check for custom
        selected_questions = 0
        has_custom = False
        for section, questions in template_data.items():
            for question in questions:
                if "custom" in question.lower() or "?" in question:
                    has_custom = True
                selected_questions += 1

        RECOMMENDED_COUNT = 100
        matches_recommended_structure = not has_custom and selected_questions == RECOMMENDED_COUNT

        # Check SQL: is a recommended template already saved?
        cursor.execute("SELECT 1 FROM templates WHERE client_id = ? AND template_name = ?", client_id, recommended_name)
        already_exists = cursor.fetchone()

        if matches_recommended_structure and already_exists:
            return jsonify({"error": "You already have a Recommended Template saved. You cannot save another using the same structure."}), 409

        # Save as Recommended if valid and first time
        if matches_recommended_structure and not already_exists:
            template_name = recommended_name
        else:
            # Otherwise treat as custom
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
