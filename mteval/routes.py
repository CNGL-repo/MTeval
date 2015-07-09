from mteval import app

from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import current_user, LoginManager, logout_user, login_required
from forms import LoginForm, RegisterForm
from database import teamDB
import loginUtils
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message


#Login manager initialisation
lm = LoginManager()
lm.init_app(app)

#mail initialisation
ts = URLSafeTimedSerializer(app.config["SECRET_KEY"]) 
mail = Mail(app)

#create an admin user if none exists
if teamDB.getAdmin() == None:
    teamDB.addTeam("admin", 
        "test@test.com",
        "admin", 
        loginUtils.hashPassword("password"), 
        isAdmin = True,
        isVerified = True, 
        isActive = True)

#Application routes
@app.route('/')
def index():
    return render_template("base.html")

@app.route('/admin')
@login_required
def adminPanel():
    if current_user.isAdmin != True:
        flash("You are not an admin")
        return redirect(url_for("index"))
    return render_template("adminPanel.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        flash("You are already logged in")
        return redirect(url_for("index"))
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        status = loginUtils.loginUser(form.teamname.data, form.password.data)
        print status
        if status["isValid"] == True:
            flash("Logged in successfully")
        else:
            flash("Login failed: " + status["reason"])

        next = request.args.get("next")
        return redirect(next or url_for("index"))
    
    else:
        return render_template("login.html", form = form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated():
        flash("You are already logged in, please log out to register a new team")
        return redirect(url_for("index"))
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        #returns dict {success: Bool, reason: String}
        res = teamDB.addTeam( 
            form.teamname.data,
            form.email.data, 
            form.organisation.data,
            loginUtils.hashPassword(form.password.data)
        )
        if res["success"] == True:
            flash("Registration successful")
            return redirect(url_for("login"))
        else: 
            flash("Registration failed: " + res["reason"])
            return redirect(url_for("register"))

    else:
        return render_template("register.html", form = form)

@lm.user_loader
def load_user(userId):
    return loginUtils.getTeamObject(userId)

@lm.unauthorized_handler
def showLoginPage():
    return redirect(url_for("login"))