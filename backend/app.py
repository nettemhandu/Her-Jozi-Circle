import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("herjozicircle.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Signup
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fullname = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("herjozicircle.db")
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (fullname, email, password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return "This email is already registered. Please log in."

        conn.close()
        return redirect(url_for("events", user=fullname))

    return render_template("signup.html")

# Login
@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("herjozicircle.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE email = ? AND password = ?", (email, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return redirect(url_for("events", user=user[0]))
    else:
        return "Invalid login, please try again."

# Events page
@app.route("/events")
def events():
    user = request.args.get("user")
    return render_template("events.html", user=user)

# Debug: show all users
def show_users():
    conn = sqlite3.connect("herjozicircle.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    print("Users in DB:", users)

show_users()

if __name__ == "__main__":
    app.run(debug=True)
