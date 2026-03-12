from flask import Flask, jsonify, request, render_template_string, redirect, url_for

app = Flask(__name__)

students = [
    {"id":1,"name":"Juan","grade":85,"section":"Stallman"},
    {"id":2,"name":"Maria","grade":90,"section":"Stallman"},
    {"id":3,"name":"Pedro","grade":70,"section":"Zion"}
]

# HOME
@app.route("/")
def home():
    return redirect(url_for("students_page"))

# STUDENT LIST
@app.route("/students")
def students_page():

    html = """
    <html>
    <head>
    <title>Student Management</title>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
    body{
    font-family:Arial;
    background:#f2f2f2;
    text-align:center;
    }

    h1{
    background:#2c3e50;
    color:white;
    padding:15px;
    }

    table{
    margin:auto;
    border-collapse:collapse;
    background:white;
    width:70%;
    }

    th,td{
    padding:10px;
    border:1px solid #ccc;
    }

    th{
    background:#3498db;
    color:white;
    }

    a{
    text-decoration:none;
    color:blue;
    }

    .btn{
    background:#27ae60;
    color:white;
    padding:8px;
    }

    </style>
    </head>

    <body>

    <h1>📚 Student Management System</h1>

    <a class="btn" href="/add_form">➕ Add Student</a>

    <h2>Student List</h2>

    <table>
    <tr>
    <th>ID</th>
    <th>Name</th>
    <th>Grade</th>
    <th>Section</th>
    <th>Action</th>
    </tr>

    {% for s in students %}
    <tr>
    <td>{{s.id}}</td>
    <td>{{s.name}}</td>
    <td>{{s.grade}}</td>
    <td>{{s.section}}</td>
    <td>
    <a href="/edit/{{s.id}}">Edit</a> |
    <a href="/delete/{{s.id}}">Delete</a>
    </td>
    </tr>
    {% endfor %}
    </table>

    <br>

    <a href="/summary">📊 View Analytics</a>

    </body>
    </html>
    """

    return render_template_string(html, students=students)

# ADD FORM
@app.route("/add_form")
def add_form():

    html="""
    <h2>Add Student</h2>

    <form action="/add_student" method="POST">

    Name:<br>
    <input name="name"><br><br>

    Grade:<br>
    <input type="number" name="grade"><br><br>

    Section:<br>
    <input name="section"><br><br>

    <button type="submit">Add Student</button>

    </form>

    <br>
    <a href="/students">Back</a>
    """

    return render_template_string(html)

# ADD STUDENT
@app.route("/add_student", methods=["POST"])
def add_student():

    new_id=len(students)+1

    students.append({
        "id":new_id,
        "name":request.form["name"],
        "grade":int(request.form["grade"]),
        "section":request.form["section"]
    })

    return redirect(url_for("students_page"))

# EDIT STUDENT
@app.route("/edit/<int:id>", methods=["GET","POST"])
def edit(id):

    student=next((s for s in students if s["id"]==id),None)

    if request.method=="POST":

        student["name"]=request.form["name"]
        student["grade"]=int(request.form["grade"])
        student["section"]=request.form["section"]

        return redirect(url_for("students_page"))

    html="""
    <h2>Edit Student</h2>

    <form method="POST">

    Name:<br>
    <input name="name" value="{{s.name}}"><br><br>

    Grade:<br>
    <input type="number" name="grade" value="{{s.grade}}"><br><br>

    Section:<br>
    <input name="section" value="{{s.section}}"><br><br>

    <button type="submit">Update</button>

    </form>

    <br>
    <a href="/students">Back</a>
    """

    return render_template_string(html, s=student)

# DELETE STUDENT
@app.route("/delete/<int:id>")
def delete(id):

    global students
    students=[s for s in students if s["id"]!=id]

    return redirect(url_for("students_page"))

# ANALYTICS
@app.route("/summary")
def summary():

    grades=[s["grade"] for s in students]

    avg=sum(grades)/len(grades)

    passed=len([g for g in grades if g>=75])
    failed=len(grades)-passed

    html="""
    <html>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <h2>📊 Student Analytics</h2>

    <p>Average Grade: {{avg}}</p>
    <p>Passed: {{passed}}</p>
    <p>Failed: {{failed}}</p>

    <canvas id="chart" width="300"></canvas>

    <script>
    var ctx=document.getElementById('chart');

    new Chart(ctx,{
        type:'pie',
        data:{
            labels:['Passed','Failed'],
            datasets:[{
                data:[{{passed}},{{failed}}]
            }]
        }
    });
    </script>

    <br>
    <a href="/students">Back</a>

    </html>
    """

    return render_template_string(html,avg=avg,passed=passed,failed=failed)

if __name__=="__main__":
    app.run()
