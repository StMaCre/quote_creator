from flask import Flask, flash, redirect, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import sqlite3
from functools import wraps

app = Flask(__name__)

# Ensure that templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create a list for the dictionnaries to be loaded
LIST = []

# Configure the databases
sqliteConnection = sqlite3.connect(
    'static/price1.sqlite', check_same_thread=False)
cursor = sqliteConnection.cursor()

# Create a new database to store the data
Connection = sqlite3.connect('static/data.sqlite')
crs = Connection.cursor()

# Define function login required


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user id
    session.clear()

    if request.method == "POST":
        # Validate the username and password
        name = request.form.get('username')
        password = request.form.get('password')
        if not name:
            return render_template("failure.html", message="You must provide a username")
        elif not password:
            return render_template("failure.html", message="You must provide a password")
        # Query database for username
        rows = cursor.execute(
            "SELECT * FROM users WHERE name = ?", (name,))
        rows = list(rows)
        # Check username exists and password is correct
        if len(rows) != 1 or rows[0][1] != password:
            return render_template("failure.html", message="invalid username and/or password")
        # Remember zhich user has logged in and password
        session["user_id"] = rows[0][0]
        return render_template("index.html")
    else:
        return render_template("login.html")


@app.route("/code", methods=["GET", "POST"])
@login_required
# validate submission
def checking():
    if request.method == "POST":
        # validate name
        code = request.form.get("code")
        if not code:
            return render_template("failure.html", message="Missing code")
        # Get information from the database
        # for the price
        cursor.execute(
            "SELECT PVP FROM price1 WHERE Referencia = (?) ", (code,))
        price = cursor.fetchall()[0][0]
        # for the name
        cursor.execute(
            "SELECT Modelo FROM price1 WHERE Referencia = (?) ", (code,))
        name = cursor.fetchall()[0][0]

        # Store the data into a dictionnary
        dict = {"code": code, "name": name, "price": price}
        LIST.append(dict)

        return render_template("code.html", LIST=LIST)
    else:
        return render_template("code.html", LIST=LIST)


@app.route("/table")
@login_required
def table():
    return render_template("code.html", LIST=LIST)

# Route to clear the table


@app.route("/clear")
@login_required
def clear():
    LIST.clear()
    return render_template("index.html", LIST=LIST)


@app.route("/delete")
@login_required
def delete():
    LIST.pop()
    return render_template("code.html", LIST=LIST)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
