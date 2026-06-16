from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    student = db.get_all_students()
    return jsonify(student), 200

@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    student_data = request.json
    try:
        student_mark = student_data["mark"]
    except:
        student_mark = 0

    try:
        student_course = student_data["course"]
    except:
        student_course = ""

    try:
        student_name = student_data["name"]
    except:
        student_name = ""



    new_stud = db.insert_student(student_name, student_course, student_mark)
    return jsonify(new_stud), 200

@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.json
    updated = db.update_student(student_id, student_data["name"], student_data["course"], student_data["mark"])
    if updated is None:
        return jsonify("id not found"), 404
    return jsonify(updated), 200

@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    student = db.delete_student(student_id)
    if student is None:
        return jsonify("id not found"), 404
    return jsonify(student), 200



@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    students = db.get_all_students()
    marks = []
    for student in students:
        marks.append(student["mark"])
    count = len(marks)
    if count != 0:
        average = sum(marks) / len(marks)
    else:
        average = 0
    minimum = min(marks)
    maxaximum = max(marks)
    return jsonify({"count": count, "average": average, "min": minimum, "max": maxaximum}), 200

@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
