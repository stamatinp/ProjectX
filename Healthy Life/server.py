from flask import Flask, render_template, request, redirect, session
from services.users import authenticate, requires_auth

app = Flask(__name__, static_folder="static")

@app.route("/")
def index():
    return render_template("/index.html", current_page='home')


@app.route("/register")
def register():
    return render_template("/users/register.html", current_page='register')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("/users/login.html", current_page='login')

    username = request.form.get("username")
    password = request.form.get("password")

    authenticated, context = authenticate(username, password)

    if authenticated:
        session["username"] = username
        session["admin"] = context.get("admin", False)
        
        return redirect("/main")
    else:
        return render_template("/users/login.html", **context, current_page='login')

bmi_categories = {
    (0, 18.5): 'Underweight',
    (18.5, 24.9): 'Normal weight',
    (24.9, 29.9): 'Overweight',
    (29.9, float('inf')): 'Obesity'
}
def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return round(bmi,)

def get_bmi_category(bmi):
    """
    Get the corresponding BMI category based on the calculated BMI.
    """
    for category_range, category in bmi_categories.items():
        if category_range[0] <= bmi < category_range[1]:
            return category
    return 'Unknown'

@app.route('/bmi', methods=['GET', 'POST'])    
def bmi():
    bmi = None
    category = None

    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        bmi = calculate_bmi(weight, height)
        category = get_bmi_category(bmi)

    if 'reset' in request.form:
        weight = None
        height = None
        bmi = None
        category = None
        
        
    return render_template('bmi.html', bmi=bmi, category=category) 







    
app.run('0.0.0.0', 80, debug=True)