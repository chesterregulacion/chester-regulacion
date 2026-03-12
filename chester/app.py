from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

# ---------------------------
# SAMPLE DATABASE (TEMP DATA)
# ---------------------------
students = [
    {"id": 1, "name": "Juan", "grade": 85, "section": "Stallman"},
    {"id": 2, "name": "Maria", "grade": 90, "section": "Stallman"},
    {"id": 3, "name": "Pedro", "grade": 70, "section": "Zion"}
]

# ---------------------------
# HOME PAGE
# ---------------------------
@app.route('/')
def home():
    return redirect(url_for('list_students'))


# ---------------------------
# VIEW ALL STUDENTS
# ---------------------------
@app.route('/students')
def list_students():

    html = """
    <h1>📚 Student Management System</h1>

    <a href="/add_student_form">➕ Add Student</a>
    <br><br>

    <a href="/summary">📊 View Analytics Summary</a>

    <hr>

    <h2>Student List</h2>

    <ul>
    {% for s in students %}
        <li>
        ID: {{s.id}} - {{s.name}} 
        (Grade: {{s.grade}}, Section: {{s.section}})

        [<a href="/student/{{s.id}}">View</a>]

        [<a href="/edit_student/{{s.id}}">Edit</a>]

        [<a href="/delete_student/{{s.id}}">Delete</a>]
        </li>
    {% endfor %}
    </ul>
    """

    return render_template_string(html, students=students)


# ---------------------------
# VIEW SINGLE STUDENT
# ---------------------------
@app.route('/student/<int:id>')
def get_student(id):

    student = next((s for s in students if s["id"] == id), None)

    if not student:
        return "Student not found", 404

    return jsonify(student)


# ---------------------------
# ADD STUDENT FORM
# ---------------------------
@app.route('/add_student_form')
def add_student_form():

    html = """
    <h2>Add New Student</h2>

    <form action="/add_student" method="POST">

    Name:
    <input type="text" name="name" required>
    <br><br>

    Grade:
    <input type="number" name="grade" required>
    <br><br>

    Section:
    <input type="text" name="section" required>
    <br><br>

    <button type="submit">Add Student</button>

    </form>

    <br>

    <a href="/students">Back to Student List</a>
    """

    return render_template_string(html)


# ---------------------------
# ADD STUDENT (POST)
# ---------------------------
@app.route('/add_student', methods=['POST'])
def add_student():

    name = request.form.get("name")
    grade = int(request.form.get("grade"))
    section = request.form.get("section")

    new_id = len(students) + 1

    new_student = {
        "id": new_id,
        "name": name,
        "grade": grade,
        "section": section
    }

    students.append(new_student)

    return redirect(url_for('list_students'))


# ---------------------------
# EDIT STUDENT
# ---------------------------
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):

    student = next((s for s in students if s["id"] == id), None)

    if not student:
        return "Student not found", 404

    if request.method == "POST":

        student["name"] = request.form["name"]
        student["grade"] = int(request.form["grade"])
        student["section"] = request.form["section"]

        return redirect(url_for('list_students'))

    html = """
    <h2>Edit Student</h2>

    <form method="POST">

    Name:
    <input type="text" name="name" value="{{student.name}}">
    <br><br>

    Grade:
    <input type="number" name="grade" value="{{student.grade}}">
    <br><br>

    Section:
    <input type="text" name="section" value="{{student.section}}">
    <br><br>

    <button type="submit">Update Student</button>

    </form>

    <br>

    <a href="/students">Back</a>
    """

    return render_template_string(html, student=student)


# ---------------------------
# DELETE STUDENT
# ---------------------------
@app.route('/delete_student/<int:id>')
def delete_student(id):

    global students

    students = [s for s in students if s["id"] != id]

    return redirect(url_for('list_students'))


# ---------------------------
# ANALYTICS SUMMARY
# ---------------------------
@app.route('/summary')
def summary():

    grades = [s["grade"] for s in students]

    if len(grades) == 0:
        return jsonify({"message": "No students available"})

    average = sum(grades) / len(grades)

    passed = len([g for g in grades if g >= 75])
    failed = len(grades) - passed

    return jsonify({
        "average_grade": average,
        "passed_students": passed,
        "failed_students": failed,
        "total_students": len(grades)
    })


if __name__ == "__main__":
    app.run()
