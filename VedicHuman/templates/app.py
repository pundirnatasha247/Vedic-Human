
from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3
import os

print("DB PATH:", os.path.abspath("database/users.db"))
app = Flask(__name__)
app.secret_key = "vedic_human_secret"   # session ke liye
app.config['SESSION_COOKIE_SAMESITE'] = "Lax"
app.config['SESSION_COOKIE_SECURE'] = False

# -----------------------------
# DATABASE SETUP (AUTO CREATE)
# -----------------------------
if not os.path.exists("database"):
    os.makedirs("database")

conn = sqlite3.connect("database/users.db")
conn.row_factory = sqlite3.Row  
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
    print("before query execution.")
    cursor.execute(
        "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
        (name, email, password)
    )
    print("after query execution.....")
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
        session["user_id"] = user[0]   # 👈 yaha add karo
        session["user_name"] = user[1]

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

#start-session
@app.route("/start-session", methods=["POST"])
def start_session():
    print("🔥 START SESSION ROUTE HIT")   # 👈 add this

    if "user_id" not in session:
        print("❌ NO USER ID IN SESSION")
        return jsonify({"success": False})

    user_id = session["user_id"]
    print("USER ID:", user_id)

    conn = sqlite3.connect("database/users.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET sessions = sessions + 1,
            minutes = minutes + 20
        WHERE id = ?
    """, (user_id,))

    conn.commit()
    conn.close()

    print("✅ DB UPDATED")

    return jsonify({"success": True})

    # Update session count + minutes
    cursor.execute("""
        UPDATE users
        SET sessions = sessions + 1,
            minutes = minutes + 20
        WHERE id = ?
    """, (user_id,))

    conn.commit()
    conn.close()

    return jsonify({"success": True})
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
