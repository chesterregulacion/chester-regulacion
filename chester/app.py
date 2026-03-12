from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>World Dish Finder</title>
<style>
body{
font-family: Arial;
background: linear-gradient(to right,#ffecd2,#fcb69f);
text-align:center;
padding:40px;
}

h1{
color:#333;
}

form{
margin-bottom:20px;
}

input{
padding:10px;
width:250px;
}

button{
padding:10px 20px;
background:#ff7f50;
border:none;
color:white;
cursor:pointer;
}

.card{
background:white;
padding:20px;
margin-top:20px;
border-radius:10px;
width:500px;
margin:auto;
box-shadow:0 4px 10px rgba(0,0,0,0.2);
}

img{
width:300px;
border-radius:10px;
}
</style>
</head>

<body>

<h1>🌍 World Dish Finder</h1>

<form method="GET">
<input name="dish" placeholder="Enter dish name (e.g. pasta)">
<button type="submit">Search</button>
</form>

{% if meal %}
<div class="card">
<h2>{{meal['strMeal']}}</h2>
<p><b>Country:</b> {{meal['strArea']}}</p>

<img src="{{meal['strMealThumb']}}">

<h3>Instructions</h3>
<p>{{meal['strInstructions'][:400]}}...</p>
</div>
{% endif %}

</body>
</html>
"""

@app.route("/", methods=["GET"])
def home():

    dish = request.args.get("dish")
    meal = None

    if dish:
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={dish}"
        data = requests.get(url).json()

        if data["meals"]:
            meal = data["meals"][0]

    return render_template_string(HTML, meal=meal)

if __name__ == "__main__":
    app.run()
