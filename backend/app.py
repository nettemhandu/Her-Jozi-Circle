import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Create users table if it doesn't exist
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

# Call the function to initialize DB
init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("herjozicircle.db")
        cursor = conn.cursor()

        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                           (name, email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            # Email already exists
            return "This email is already registered. Please log in."

        conn.close()
        return redirect(url_for("events", message=f"Welcome {name}! You signed up with {email}."))

    return render_template("signup.html")



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
        return redirect(url_for("events", message=f"Welcome back {user[0]}!"))
    else:
        return "Invalid login, please try again."


@app.route("/events")
def events():
    user = request.args.get("user")  # get the name from the URL
    return render_template("events.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
    
    
 # debugging tool for viewing database info
def show_users():
    conn = sqlite3.connect("herjozicircle.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    print("📌 Current users in DB:", users)

show_users()
