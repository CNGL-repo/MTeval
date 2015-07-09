from mteval import app, lm

from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import login_required, current_user
from forms import LoginForm, RegisterForm
from database import teamDB
import loginUtils

@login_required
@app.route('/')
def index():
    print current_user.is_authenticated()
    return render_template("base.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        status = loginUtils.loginUser(form.teamname.data, form.password.data)
        print status
        if status["isValid"] == True:
            flash("Logged in successfully")
        else:
            flash("Login failed")

        next = request.args.get("next")
        return redirect(next or url_for("index"))
    
    else:
        return render_template("login.html", form = form)

@app.route('/register', methods=["GET", "POST"])
def register():
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
    return teamDB.getTeamById(userId)