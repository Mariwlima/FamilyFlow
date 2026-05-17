import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///family.db")
with app.app_context():
    db.execute("""CREATE TABLE IF NOT EXISTS families (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL UNIQUE, password TEXT NOT NULL)""")
    db.execute("""CREATE TABLE IF NOT EXISTS members (id INTEGER PRIMARY KEY AUTOINCREMENT, family_id INTEGER NOT NULL, name TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'adult', color TEXT DEFAULT '#4A90D9')""")
    db.execute("""CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, family_id INTEGER NOT NULL, member_id INTEGER NOT NULL, title TEXT NOT NULL, date TEXT NOT NULL, time TEXT)""")
    db.execute("""CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, family_id INTEGER NOT NULL, member_id INTEGER NOT NULL, title TEXT NOT NULL, due_date TEXT, done INTEGER NOT NULL DEFAULT 0)""")
    db.execute("""CREATE TABLE IF NOT EXISTS shopping (id INTEGER PRIMARY KEY AUTOINCREMENT, family_id INTEGER NOT NULL, item TEXT NOT NULL, done INTEGER NOT NULL DEFAULT 0)""")
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    if not session.get("family_id"):
        return redirect("/login")
    
    member = session.get("member")
    if member and member["role"] == "child":
        return redirect("/child")
    
    return redirect("/dashboard")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        member_name = request.form.get("member_name")
        
        if not name or not password or not member_name:
            flash("Please fill all fields", "danger")
            return redirect("/login")
        
        family = db.execute("SELECT * FROM families WHERE name = ?", name)
        
        if len(family) != 1 or not check_password_hash(family[0]["password"], password):
            flash("Invalid family name or password", "danger")
            return redirect("/login")
        
        member = db.execute(
            "SELECT * FROM members WHERE family_id = ? AND name = ?",
            family[0]["id"], member_name
        )
        
        if len(member) != 1:
            flash("Member not found", "danger")
            return redirect("/login")
        
        session["family_id"] = family[0]["id"]
        session["member"] = member[0]
        
        if member[0]["role"] == "child":
            return redirect("/child")
        return redirect("/dashboard")
    
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        members = request.form.getlist("members")
        roles = request.form.getlist("roles")
        
        if not name or not password or not confirmation:
            flash("Please fill all fields", "danger")
            return redirect("/register")
        
        if password != confirmation:
            flash("Passwords don't match", "danger")
            return redirect("/register")
        
        try:
            family_id = db.execute(
                "INSERT INTO families (name, password) VALUES (?, ?)",
                name, generate_password_hash(password)
            )
        except:
            flash("Family name already exists", "danger")
            return redirect("/register")
        
        for i, member in enumerate(members):
            if member:
                db.execute(
                    "INSERT INTO members (family_id, name, role) VALUES (?, ?, ?)",
                    family_id, member, roles[i]
                )
        
        flash("Family registered! Please log in.", "success")
        return redirect("/login")
    
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/dashboard")
def dashboard():
    if not session.get("family_id"):
        return redirect("/login")
    
    members = db.execute(
        "SELECT * FROM members WHERE family_id = ?", session["family_id"]
    )
    events = db.execute(
        "SELECT e.*, m.name as member_name, m.color FROM events e JOIN members m ON e.member_id = m.id WHERE e.family_id = ? ORDER BY e.date, e.time",
        session["family_id"]
    )
    tasks = db.execute(
        "SELECT t.*, m.name as member_name FROM tasks t JOIN members m ON t.member_id = m.id WHERE t.family_id = ? AND t.done = 0 ORDER BY t.due_date",
        session["family_id"]
    )
    shopping = db.execute(
        "SELECT * FROM shopping WHERE family_id = ? AND done = 0",
        session["family_id"]
    )
    
    return render_template("dashboard.html",
        members=members,
        events=events,
        tasks=tasks,
        shopping=shopping,
        member=session["member"]
    )

@app.route("/events", methods=["GET", "POST"])
def events():
    if not session.get("family_id"):
        return redirect("/login")
    
    if request.method == "POST":
        title = request.form.get("title")
        date = request.form.get("date")
        time = request.form.get("time")
        member_id = request.form.get("member_id")
        
        if not title or not date or not member_id:
            flash("Please fill all fields", "danger")
            return redirect("/events")
        
        db.execute(
            "INSERT INTO events (family_id, member_id, title, date, time) VALUES (?, ?, ?, ?, ?)",
            session["family_id"], member_id, title, date, time
        )
        flash("Event added!", "success")
        return redirect("/dashboard")
    
    members = db.execute(
        "SELECT * FROM members WHERE family_id = ?", session["family_id"]
    )
    return render_template("events.html", members=members)

@app.route("/events/delete/<int:event_id>")
def delete_event(event_id):
    if not session.get("family_id"):
        return redirect("/login")
    db.execute("DELETE FROM events WHERE id = ? AND family_id = ?", event_id, session["family_id"])
    return redirect("/dashboard")

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if not session.get("family_id"):
        return redirect("/login")
    
    if request.method == "POST":
        title = request.form.get("title")
        member_id = request.form.get("member_id")
        due_date = request.form.get("due_date")
        
        if not title or not member_id:
            flash("Please fill all fields", "danger")
            return redirect("/tasks")
        
        db.execute(
            "INSERT INTO tasks (family_id, member_id, title, due_date, done) VALUES (?, ?, ?, ?, 0)",
            session["family_id"], member_id, title, due_date
        )
        flash("Task added!", "success")
        return redirect("/dashboard")
    
    members = db.execute(
        "SELECT * FROM members WHERE family_id = ?", session["family_id"]
    )
    return render_template("tasks.html", members=members)

@app.route("/tasks/done/<int:task_id>")
def done_task(task_id):
    if not session.get("family_id"):
        return redirect("/login")
    db.execute("UPDATE tasks SET done = 1 WHERE id = ? AND family_id = ?", task_id, session["family_id"])
    return redirect("/dashboard")

@app.route("/shopping", methods=["GET", "POST"])
def shopping():
    if not session.get("family_id"):
        return redirect("/login")
    
    if request.method == "POST":
        item = request.form.get("item")
        
        if not item:
            flash("Please enter an item", "danger")
            return redirect("/shopping")
        
        db.execute(
            "INSERT INTO shopping (family_id, item, done) VALUES (?, ?, 0)",
            session["family_id"], item
        )
        flash("Item added!", "success")
        return redirect("/dashboard")
    
    items = db.execute(
        "SELECT * FROM shopping WHERE family_id = ?", session["family_id"]
    )
    return render_template("shopping.html", items=items)

@app.route("/shopping/done/<int:item_id>")
def done_shopping(item_id):
    if not session.get("family_id"):
        return redirect("/login")
    db.execute("UPDATE shopping SET done = 1 WHERE id = ? AND family_id = ?", item_id, session["family_id"])
    return redirect("/dashboard")

@app.route("/shopping/delete/<int:item_id>")
def delete_shopping(item_id):
    if not session.get("family_id"):
        return redirect("/login")
    db.execute("DELETE FROM shopping WHERE id = ? AND family_id = ?", item_id, session["family_id"])
    return redirect("/dashboard")

@app.route("/child")
def child():
    if not session.get("family_id"):
        return redirect("/login")
    
    member = session["member"]
    events = db.execute(
        "SELECT * FROM events WHERE family_id = ? AND member_id = ? ORDER BY date, time",
        session["family_id"], member["id"]
    )
    tasks = db.execute(
        "SELECT * FROM tasks WHERE family_id = ? AND member_id = ? AND done = 0 ORDER BY due_date",
        session["family_id"], member["id"]
    )
    
    return render_template("child.html", member=member, events=events, tasks=tasks)