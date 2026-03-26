from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "vedic_human_secret"   # session ke liye

# -----------------------------
# DATABASE SETUP (AUTO CREATE)
# -----------------------------
if not os.path.exists("database"):
    os.makedirs("database")

conn = sqlite3.connect("database/users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    password TEXT
)
""")

conn.commit()
conn.close()

# -----------------------------
# ROUTES
# -----------------------------

# Login Page
@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")




# 🔹 Signup Logic
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data["name"]
    email = data["email"]
    password = data["password"]

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, password)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})

# 🔹 Login Logic
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        session["user_name"] = user[1]   # name store
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

# 🔹 Dashboard Route (HOME PAGE)
@app.route("/dashboard")
def dashboard():
    if "user_name" not in session:
        return redirect("/")

    return render_template(
        "dashboard.html",
        name=session["user_name"]
    )

# 🔹 Session Page
@app.route("/session")
def session_page():
    if "user_name" not in session:
        return redirect("/")
    
    return render_template("session.html")

# 🔹 Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
