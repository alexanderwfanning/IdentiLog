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
        
    }
@app.before_request
def load_db():
    connect()

def admin_required(f):
    def decorated_function(*args, **kwargs):
        is_admin = verify_admin(session['username'])
        if not is_admin:
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
                return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route("/")
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
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
            return render_template("index.html", login_message="You are logged out", organization=organization_text)
        
@app.route("/dashboard")
@login_required
def dashboard():
    if request.method == 'GET':
                is_admin = verify_admin(session['username'])
                user_dict=get_users()
                return render_template("dashboard.html", username=session['username'], organization=organization_text, users=user_dict, links=links, is_admin=is_admin)
            
@app.route("/admin")
@login_required
@admin_required
def admin():
    if request.method == 'GET':
        user_dict=get_users()
        return render_template("admin.html", username=session['username'], organization=organization_text, users=user_dict)

@app.route("/logout")
@login_required
def logout():
    if request.method == 'GET':
        username=session['username']
        user_logging(username, "Logged out")
        session.clear()
        return redirect(url_for('index'))
    
@app.route("/logs", methods=["POST", 'GET'])
@login_required
@admin_required
def logs():
    user = request.form['user']
    print(user)
    user_log = get_log(user)
    user_logging(session['username'], f"Viewed logs for {user}")
    return render_template('logs.html', organization=organization_text, user=user, user_log=user_log)
    
if __name__ == "__main__":
    app.run(debug=True)