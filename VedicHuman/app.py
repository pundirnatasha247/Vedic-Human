from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3
import os
from datetime import datetime


app = Flask(__name__)
app.secret_key = "vedic_human_secret"


# DB setup
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

cursor.execute("""
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT
)
""")

conn.commit()
conn.close()

# ROUTES
@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name,email,password) VALUES (?,?,?)",
                   (data["name"], data["email"], data["password"]))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=? AND password=?",
                   (data["email"], data["password"]))
    user = cursor.fetchone()
    conn.close()

    if user:
        session["user_id"] = user[0]
        session["user_name"] = user[1]
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")
    return render_template("dashboard.html", name=session["user_name"])

@app.route("/session")
def session_page():
    if "user_id" not in session:
        return redirect("/")
    return render_template("session.html")

@app.route("/library")
def library():
    if "user_id" not in session:
        return redirect("/")
    return render_template("library.html")

# SESSION COMPLETE
@app.route('/complete_session', methods=['POST'])
def complete_session():
    if "user_id" not in session:
        return jsonify({"status": "error"})

    user_id = session["user_id"]
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect("database/users.db",check_same_thread=False)
    cursor = conn.cursor()

    # check duplicate entry
    cursor.execute("SELECT * FROM progress WHERE user_id=? AND date=?", (user_id, today))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute("INSERT INTO progress (user_id, date) VALUES (?, ?)", (user_id, today))
        conn.commit()

    conn.close()

    return jsonify({"status": "success", "date": today})

# CALENDAR DATA
@app.route("/get_dashboard_data")
def get_dashboard_data():
    if "user_id" not in session:
        return jsonify({"dates": []})

    user_id = session["user_id"]

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT date FROM progress WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    dates = [r[0] for r in rows]

    return jsonify({"dates": dates})

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
