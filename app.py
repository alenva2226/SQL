from flask import Flask, request, render_template, redirect, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = "super_secret_key"  # Change this for security

DATABASE = "database.db"
FLAG = "NKCTF{burpsuit3_1s_f3n}"  # Hidden flag

def get_db():
    """Connects to the SQLite database."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row  # Fetch rows as dictionaries
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/", methods=["GET", "POST"])
def login():
    """Login page with SQL Injection vulnerability."""
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        # ⚠️ VULNERABLE QUERY (DO NOT USE IN REAL-WORLD APPS) ⚠️
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            session["user"] = username
            return redirect("/admin")
        
        # Check if user tried a common SQLi payload and give a hint instead
        if " OR " in username or "--" in username or " UNION " in username:
            error = "Incorrect username or password. Hint: Think outside the box!"
        else:
            error = "Incorrect username or password."

    return render_template("login.html", error=error)

@app.route("/admin")
def admin():
    """Admin page that only appears after SQLi login."""
    if "user" not in session:
        return redirect("/")
    
    return render_template("admin.html")

@app.route("/flag", methods=["GET"])
def flag():
    """Returns the flag but only through Burp Suite request interception."""
    if "user" not in session:
        return redirect("/")
    
    user_agent = request.headers.get("User-Agent", "")
    
    # Trick: Only show the flag if request is intercepted (e.g., Burp Suite)
    if "BurpSuite" in user_agent or "Mozilla" not in user_agent:
        return FLAG
    
    return "Not too easy lol !!!"

if __name__ == "__main__":
    app.run(debug=True)
