import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]

        # Connect to the database
        conn = sqlite3.connect("herjozi.db")
        cursor = conn.cursor()

        try:
            # Insert new user
            cursor.execute(
                "INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)",
                (fullname, email, password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            # If the email already exists
            conn.close()
            return "This email is already registered."
        
        conn.close()

        # Redirect to events page with welcome message
        return redirect(url_for("events", user=fullname))
    
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        # Connect to the database
        conn = sqlite3.connect("herjozi.db")
        cursor = conn.cursor()

        # Find user by email
        cursor.execute("SELECT fullname, password FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
        conn.close()

        # Check credentials
        if user and user[1] == password:
            # Login successful → redirect to events page with username
            return redirect(url_for("events", user=user[0]))
        else:
            # Login failed → show message
            return "Invalid email or password. Please try again."

    # If GET request → show login form
    return render_template("signup.html")  # or use a separate login.html


@app.route("/events")
def events():
    user = request.args.get("user")  # get the name from the URL
    return render_template("events.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
