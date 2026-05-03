from flask import Flask, render_template, request, jsonify, session, redirect
import sqlite3
import os
from datetime import datetime, timedelta, date

app = Flask(__name__)
app.secret_key = "vedic_human_secret"

DB_PATH = "database/users.db"

# DB CONNECTION
def get_connection():
    return sqlite3.connect(DB_PATH, timeout=10, check_same_thread=False)

#CREATE Db
if not os.path.exists("database"):
    os.makedirs("database")

conn = get_connection()
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
    date TEXT,
    total_time INTEGER DEFAULT 0,
    best_time INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

#  STREAK FUNCTION 
def get_streak(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date 
        FROM progress 
        WHERE user_id = ? 
        ORDER BY date DESC
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    dates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in rows]

    streak = 0
    today = date.today()

    for i, d in enumerate(dates):
        if i == 0:
            if d == today:
                streak += 1
            elif d == today - timedelta(days=1):
                streak += 1
                today = today - timedelta(days=1)
            else:
                break
        else:
            if d == today - timedelta(days=1):
                streak += 1
                today = d
            else:
                break

    return streak

# ---------------- ROUTES ----------------

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name,email,password) VALUES (?,?,?)",
        (data["name"], data["email"], data["password"])
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (data["email"], data["password"])
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        session["user_id"] = user[0]
        session["user_name"] = user[1]
        return jsonify({"success": True})

    return jsonify({"success": False})

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]
    streak = get_streak(user_id)
    best_streak = get_best_streak(user_id)

    return render_template(
    "dashboard.html",
    name=session["user_name"],
    streak=streak,
    best_streak=best_streak
)
# ---------------- SESSION PAGE ----------------
@app.route("/session")
def session_page():
    if "user_id" not in session:
        return redirect("/")
    return render_template("session.html")

# ---------------- COMPLETE SESSION ----------------
@app.route("/complete_session", methods=["POST"])
def complete_session():
    if "user_id" not in session:
        return jsonify({"status": "error"})

    data = request.get_json()
    total_time = int(data.get("total_time", 0))
    best_time = int(data.get("best_time", 0))

    user_id = session["user_id"]
    today = datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    cursor = conn.cursor()

    # Check if already exists
    cursor.execute(
        "SELECT * FROM progress WHERE user_id=? AND date=?",
        (user_id, today)
    )
    row = cursor.fetchone()

    if row:
        # UPDATE
        cursor.execute("""
            UPDATE progress 
            SET total_time = total_time + ?, 
                best_time = CASE 
                    WHEN ? > best_time THEN ? 
                    ELSE best_time 
                END
            WHERE user_id=? AND date=?
        """, (total_time, best_time, best_time, user_id, today))
    else:
        # INSERT
        cursor.execute("""
            INSERT INTO progress (user_id, date, total_time, best_time)
            VALUES (?, ?, ?, ?)
        """, (user_id, today, total_time, best_time))

    conn.commit()
    conn.close()

    return jsonify({"status": "success"})

# ---------------- CALENDAR DATA ----------------
@app.route("/get_dashboard_data")
def get_dashboard_data():
    if "user_id" not in session:
        return jsonify({"dates": []})

    user_id = session["user_id"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT date FROM progress WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    dates = [r[0] for r in rows]

    return jsonify({"dates": dates})

# ---------------- STREAK API ----------------
@app.route("/get_streak")
def get_streak_api():
    if "user_id" not in session:
        return jsonify({"streak": 0})

    user_id = session["user_id"]
    streak = get_streak(user_id)

    return jsonify({"streak": streak})
def get_best_streak(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date FROM progress 
        WHERE user_id = ? 
        ORDER BY date
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    dates = [datetime.strptime(row[0], "%Y-%m-%d").date() for row in rows]

    best = 0
    current = 0

    for i in range(len(dates)):
        if i == 0:
            current = 1
        else:
            if dates[i] == dates[i-1] + timedelta(days=1):
                current += 1
            else:
                current = 1

        best = max(best, current)

    return best
# ---OTHER PAGES -----
@app.route("/library")
def library():
    if "user_id" not in session:
        return redirect("/")
    return render_template("library.html")

@app.route("/progress")
def progress():
    if "user_id" not in session:
        return redirect("/")
    return render_template("progress.html", name=session["user_name"])

@app.route("/get_progress_data")
def get_progress_data():
    if "user_id" not in session:
        return jsonify({
            "total_sessions": 0,
            "total_minutes": 0,
            "current_streak": 0,
            "best_streak": 0
        })

    try:
        user_id = session["user_id"]
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM progress WHERE user_id=?", (user_id,))
        total_sessions = cursor.fetchone()[0]

        cursor.execute("SELECT SUM(total_time) FROM progress WHERE user_id=?", (user_id,))
        total_minutes = cursor.fetchone()[0] or 0

        current_streak = get_streak(user_id)
        best_streak = get_best_streak(user_id)

        conn.close()

        return jsonify({
            "total_sessions": total_sessions,
            "total_minutes": total_minutes,
            "current_streak": current_streak,
            "best_streak": best_streak
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "total_sessions": 0,
            "total_minutes": 0,
            "current_streak": 0,
            "best_streak": 0
        })

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/session/<yoga_name>")
def yoga_session(yoga_name):
    if "user_id" not in session:
        return redirect("/")
    return render_template("session.html", yoga=yoga_name)

@app.route("/start-session", methods=["POST"])
def start_session():
    if "user_id" not in session:
        return jsonify({"success": False})
    return jsonify({"success": True})

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)
