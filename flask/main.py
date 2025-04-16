from flask import Flask, request,jsonify
import mysql.connector
import json


app = Flask(__name__)

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '',
    database = 'student'
)


@app.route('/students',methods= ['POST'])
def add_student():
    data = request.get_json()

    # validation
    if not data:
        return jsonify({"error": "Invalid JSON input."}), 400
    if 'name' not in data or 'age' not in data or 'standard' not in data or 'subjects' not in data:
        return jsonify({"error": "Missing required fields."}), 400
    if not isinstance(data['age'], int) or data['age'] <= 0:
        return jsonify({"error": "Age must be a positive integer."}), 400
    if not isinstance(data['subjects'], list) or len(data['subjects']) == 0:
        return jsonify({"error": "Subjects must be a non-empty list."}), 400

    name = data.get('name')
    age = data.get('age') 
    standard = data.get('standard') 
    subjects = json.dumps(data['subjects']) 

    cursor = db.cursor()
    sql_query = "INSERT INTO student (name,age,standard,subjects) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql_query,(name,age,standard,subjects))
    db.commit()
    return jsonify({"message":"Data Addes Successfully."}),200


@app.route('/students', methods=['GET'])
def get_all_students():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student")
    results = cursor.fetchall()
    # Safely decode subjects
    for student in results:
        try:
            student['subjects'] = json.loads(student['subjects'])
        except (TypeError, json.JSONDecodeError):
            student['subjects'] = []  # fallback if something's wrong
    return jsonify(results), 200


@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    if not student:
        return jsonify({"error": "Student not found."}), 404
    student['subjects'] = json.loads(student['subjects'])
    return jsonify(student), 200


@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON input."}), 400

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM student WHERE id = %s", (student_id,))
    if not cursor.fetchone():
        return jsonify({"error": "Student not found."}), 404

    updates = []
    values = []

    if 'name' in data:
        updates.append("name = %s")
        values.append(data['name'])
    if 'age' in data:
        if not isinstance(data['age'], int) or data['age'] <= 0:
            return jsonify({"error": "Age must be a positive integer."}), 400
        updates.append("age = %s")
        values.append(data['age'])
    if 'standard' in data:
        updates.append("standard = %s")
        values.append(data['standard'])
    if 'subjects' in data:
        if not isinstance(data['subjects'], list) or len(data['subjects']) == 0:
            return jsonify({"error": "Subjects must be a non-empty list."}), 400
        updates.append("subjects = %s")
        values.append(json.dumps(data['subjects']))

    if not updates:
        return jsonify({"error": "No valid fields to update."}), 400

    sql = f"UPDATE student SET {', '.join(updates)} WHERE id = %s"
    values.append(student_id)
    cursor.execute(sql, tuple(values))
    db.commit()
    return jsonify({"message": "Student updated successfully."}), 200

# -------------------- DELETE --------------------
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM student WHERE id = %s", (student_id,))
    if not cursor.fetchone():
        return jsonify({"error": "Student not found."}), 404

    cursor.execute("DELETE FROM student WHERE id = %s", (student_id,))
    db.commit()
    return jsonify({"message": "Student deleted successfully."}), 200

if __name__ == "__main__":
    print("Connecting to db...")
    app.run()
