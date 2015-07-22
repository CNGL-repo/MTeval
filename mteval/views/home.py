from flask import Blueprint, Flask, render_template, request, send_file, redirect, url_for, Response, flash
from flask.ext.login import request, current_user, LoginManager, logout_user, login_required
from mteval.forms import LoginForm, RegisterForm, EditTeamForm, CompetitionForm, CompetitionEditForm
from mteval.database import teamDB, compDB
from werkzeug import secure_filename
import os
from mteval import loginUtils

home = Blueprint("home", __name__)


#Application routes
@home.route('/')
def index():
    upcomingComps = compDB.getUpcomingCompList()
    return render_template("home/index.html", upcomingComps=upcomingComps)


###Login & registration routes
@home.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        flash("You are already logged in")
        return redirect(url_for("home.index"))
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        status = loginUtils.loginUser(form.teamname.data, form.password.data)
        print status
        if status["isValid"] == True:
            flash("Logged in successfully")
        else:
            flash("Login failed: " + status["reason"])

        next = request.args.get("next")
        return redirect(next or url_for("home.index"))
    
    else:
        return render_template("home/login.html", form = form)

@home.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.login"))

@home.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated():
        flash("You are already logged in, please log out to register a new team")
        return redirect(url_for("home.index"))
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
            return redirect(url_for("home.login"))
        else: 
            flash("Registration failed: " + res["reason"])
            return redirect(url_for("home.register"))

    return render_template("home/register.html", form = form)

