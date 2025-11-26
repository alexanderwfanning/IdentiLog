from flask import Flask, render_template, request, session, redirect, url_for
from app.db.db_utils import verify_user, new_user, connect, get_users
from app.config.config import Config
app = Flask(__name__)
key = Config()
app.secret_key = key.flask_key
organization_text = key.organization_text
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
            return render_template("index.html", login_message=status)
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
                user_dict=get_users()
                return render_template("dashboard.html", username=session['username'], organization=organization_text, users=user_dict)
            case False:
                return redirect(url_for('login'))

@app.route("/logout")
def logout():
    if request.method == 'GET':
        session.clear()
        return redirect(url_for('index'))