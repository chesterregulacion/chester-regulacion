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
    background:#f4f6f9;
    text-align:center;
    margin:0;
    }

    h1{
    background:#2c3e50;
    color:white;
    padding:20px;
    margin:0;
    }

    table{
    margin:auto;
    border-collapse:collapse;
    background:white;
    width:70%;
    box-shadow:0 0 10px rgba(0,0,0,0.2);
    }

    th,td{
    padding:12px;
    border:1px solid #ddd;
    }

    th{
    background:#3498db;
    color:white;
    }

    tr:hover{
    background:#f2f2f2;
    }

    a{
    text-decoration:none;
    }

    .btn{
    background:#27ae60;
    color:white;
    padding:10px 15px;
    border-radius:5px;
    margin:10px;
    display:inline-block;
    }

    .btn:hover{
    background:#219150;
    }

    .link{
    color:#2980b9;
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
    <a class="link" href="/edit/{{s.id}}">Edit</a> |
    <a class="link" href="/delete/{{s.id}}">Delete</a>
    </td>
    </tr>
    {% endfor %}
    </table>

    <br>
    <a class="btn" href="/summary">📊 View Analytics</a>

    </body>
    </html>
    """

    return render_template_string(html, students=students)

# ADD FORM
@app.route("/add_form")
def add_form():

    html="""
    <html>
    <head>

    <style>

    body{
    font-family:Arial;
    background:#ecf0f1;
    text-align:center;
    }

    .form-box{
    background:white;
    width:350px;
    margin:auto;
    padding:30px;
    border-radius:10px;
    box-shadow:0 0 10px rgba(0,0,0,0.2);
    margin-top:50px;
    }

    input{
    width:90%;
    padding:10px;
    margin:5px;
    border:1px solid #ccc;
    border-radius:5px;
    }

    button{
    background:#27ae60;
    color:white;
    padding:10px;
    width:95%;
    border:none;
    border-radius:5px;
    cursor:pointer;
    }

    button:hover{
    background:#219150;
    }

    a{
    text-decoration:none;
    color:#2980b9;
    }

    </style>

    </head>

    <body>

    <div class="form-box">

    <h2>➕ Add Student</h2>

    <form action="/add_student" method="POST">

    <input name="name" placeholder="Student Name" required><br>

    <input type="number" name="grade" placeholder="Grade" required><br>

    <input name="section" placeholder="Section" required><br><br>

    <button type="submit">Add Student</button>

    </form>

    <br>
    <a href="/students">⬅ Back</a>

    </div>

    </body>
    </html>
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
    <html>
    <body style="font-family:Arial;text-align:center;background:#ecf0f1;">

    <div style="background:white;width:350px;margin:auto;padding:30px;border-radius:10px;margin-top:50px;box-shadow:0 0 10px rgba(0,0,0,0.2);">

    <h2>Edit Student</h2>

    <form method="POST">

    <input name="name" value="{{s.name}}"><br><br>

    <input type="number" name="grade" value="{{s.grade}}"><br><br>

    <input name="section" value="{{s.section}}"><br><br>

    <button style="background:#3498db;color:white;padding:10px;border:none;border-radius:5px;">Update</button>

    </form>

    <br>
    <a href="/students">Back</a>

    </div>

    </body>
    </html>
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

    avg=round(sum(grades)/len(grades),2)

    passed=len([g for g in grades if g>=75])
    failed=len(grades)-passed

    html="""
    <html>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <body style="font-family:Arial;text-align:center;background:#f4f6f9;">

    <h2>📊 Student Analytics</h2>

    <p><b>Average Grade:</b> {{avg}}</p>
    <p><b>Passed:</b> {{passed}}</p>
    <p><b>Failed:</b> {{failed}}</p>

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

    <br><br>
    <a href="/students">⬅ Back</a>

    </body>
    </html>
    """

    return render_template_string(html,avg=avg,passed=passed,failed=failed)

if __name__=="__main__":
    app.run(debug=True)
