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
        return redirect(url_for("events", user=fullname))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        return redirect(url_for("events"))
    return render_template("signup.html")

@app.route("/events")
def events():
    user = request.args.get("user")  # get the name from the URL
    return render_template("events.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)
