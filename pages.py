from flask import Flask, render_template, request, session, redirect, url_for
from app.db.db_utils import verify_user, new_user, connect, get_users, user_logging, get_log, verify_admin
from app.config.config import Config
app = Flask(__name__)
key = Config()
app.secret_key = key.flask_key
organization_text = key.organization_text
links = {
        "Google": "https://google.com",
        "GitHub": "https://github.com",
        "Stack Overflow": "https://stackoverflow.com",
        # Add as many as you need
    }
@app.before_request
def load_db():
    connect()

@app.route("/")
def index():
    # Session cookie:
    if 'username' in session:
         return redirect("/dashboard")
    # No session cookie:
    return render_template("index.html", organization=organization_text)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template("register.html")
    elif request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form['email']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        organization_key = request.form['organization_key']
        print(f'{username}, {password}, {confirm_password}, {email}, {firstname}, {lastname}, {organization_key}')
        registered, status = new_user(username, password, confirm_password, firstname, lastname, email, organization_key)
        if registered:
            return render_template("index.html", login_message=status, organization=organization_text)
        if not registered:
            return render_template("register.html", register_message=status)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        authenticated, invalid_credential = verify_user(username, password)
        if authenticated:
            session['username'] = request.form['username']
            if 'remember_me' in request.form:
                session.permanent = True
            return render_template("login.html")
        else:
            return render_template("index.html", login_message=invalid_credential)
    elif request.method == 'GET':
        if 'username' in session:
            return render_template("login.html")
        else:
            return render_template("index.html", login_message="You are logged out")
        
@app.route("/dashboard")
def dashboard():
    if request.method == 'GET':
        match 'username' in session:
            case True:
                is_admin = verify_admin(session['username'])
                user_dict=get_users()
                return render_template("dashboard.html", username=session['username'], organization=organization_text, users=user_dict, links=links, is_admin=is_admin)
            case False:
                return redirect(url_for('login'))
            
@app.route("/admin")
def admin():
    if request.method == 'GET':
        match 'username' in session:
            case True:
                user_dict=get_users()
                return render_template("admin.html", username=session['username'], organization=organization_text, users=user_dict)
            case False:
                return redirect(url_for('login'))

@app.route("/logout")
def logout():
    if request.method == 'GET':
        username=session['username']
        user_logging(username, "Logged out")
        session.clear()
        return redirect(url_for('index'))
    
@app.route("/logs", methods=["POST"])
def logs():
    is_admin = verify_admin(session['username'])
    if is_admin:
        if request.method == "POST":
            user = request.form['user']
            print(user)
            user_log = get_log(user)
            user_logging(session['username'], f"Viewed logs for {user}")
        return render_template('logs.html', organization=organization_text, user=user, user_log=user_log)
    else:
        return redirect(url_for('index'))