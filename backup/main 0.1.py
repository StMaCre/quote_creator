from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
import sqlite3
import flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Ensure that templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Create a list for the dictionnaries to be loaded
LIST = []

# Use the SQL database
sqliteConnection = sqlite3.connect(
    'static/price1.sqlite', check_same_thread=False)
cursor = sqliteConnection.cursor()

# Create a new database to store the data  (TO DO)
Connection = sqlite3.connect('static/data.sqlite')
crs = Connection.cursor()


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
        if not request.form.get("username"):
            return render_template("failure.html", message="You must provide a username")
        elif not request.form.get("password"):
            return render_template("failure.html", message="You must provide a password")
        return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/code", methods=["GET", "POST"])
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
def table():
    return render_template("code.html", LIST=LIST)

# Route to clear the table


@app.route("/clear")
def clear():
    LIST.clear()
    return render_template("index.html", LIST=LIST)


@app.route("/delete")
def delete():
    LIST.pop()
    return render_template("code.html", LIST=LIST)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
