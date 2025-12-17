import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize database
def init_db():
    conn = sqlite3.connect("herjozicircle.db")
    cursor = conn.cursor()
    
    # users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
    )''')
    
    # events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT,
            description TEXT
    )''')
    
    # rsvp table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rsvp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            event_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(event_id) REFERENCES events(id)
        )''')
    
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
        # Pass action=signup
        return redirect(url_for("events", user=fullname, action="signup"))

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
        # Pass action=login
        return redirect(url_for("events", user=user[0], action="login"))
    else:
        return "Invalid login, please try again."
    


# Events page
@app.route("/events")
def events():
    user = request.args.get("user")
    action = request.args.get("action")  # either "signup" or "login"
    return render_template("events.html", user=user, action=action)

# # Debug: show all users
# def show_users():
#     conn = sqlite3.connect("herjozicircle.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users")
#     users = cursor.fetchall()
#     conn.close()
#     print("Users in DB:", users)

# show_users()

# RSVP

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

results_obj = {
    "errors" : [],
    "values" : [{}]
}