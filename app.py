import sqlite3
from flask import Flask,render_template, request, redirect, url_for

app = Flask(__name__)

WEATHER_API_KEY = "7dd26626d28e8f5a08b800cc9c488f45"
city = "Johannesburg"

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

# Helper Methods for Weather API

def get_weather_data(city):
    """
    This function gets weather data from an API
    It returns temperature, description, and icon URL
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        data = response.json
        
        if response.status_code == 200:
            return {
                'temp': data['main']['temp'],  # Temperature in Celsius
                'description': data['weather'][0]['description'],  # Like "clear sky"
                'icon': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"  # Weather icon
            }
    except Exception as e:
        print(f"Error getting weather: {e}")
    
    return None

def generate_message(temp, description):
    """
    This function creates a running recommendation based on weather
    """
    description_lower = description.lower()
    
    if temp >= 10 and temp <= 30 and 'rain' not in description_lower and 'snow' not in description_lower:
        return "Great weather for outdoors today :)"
    else:
        return "Weather conditions may not be ideal for outdoors. Rain check :)"

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