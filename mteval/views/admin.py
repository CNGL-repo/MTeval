from mteval import app, loginUtils
from flask import Blueprint, Flask, render_template, request, send_file, redirect, url_for, Response, flash
from flask.ext.login import request, current_user, LoginManager, logout_user, login_required
from itsdangerous import URLSafeTimedSerializer
from mteval.database import teamDB, compDB
from flask_mail import Mail, Message

admin = Blueprint("admin", __name__)

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
        emailVerified = True, 
        isActive = True)


#Route for admin panel, where the admin can do various tasks
@admin.route('/admin')
@login_required
def adminPanel():
    if current_user.isAdmin != True:
        flash("You are not an admin")
        return redirect(url_for("home.index"))

    #perhaps it might be better to get all teams once and then check for conditions in template?
    #rather than querying twice and passing a lot of redundant information 
    pendingTeams = teamDB.getPendingTeams()
    teams = teamDB.getTeamList()
    return render_template("admin/adminPanel.html", pendingTeams=pendingTeams, teams=teams)


@admin.route("/admin/acceptTeam/<teamName>")
def acceptTeam(teamName):
    if current_user.isAdmin != True:
        flash("You are not permitted to do this")
        return redirect(url_for("home.index"))


    team = teamDB.getTeamByName(teamName)
    
    token = ts.dumps(team["email"], salt='email-confirm-key')
    confirm_url = url_for(
        'admin.confirmEmail',
        token = token,
        _external = True)

    html = render_template(
        'admin/verification.html',
        confirm_url = confirm_url)

    email = team["email"]
    msg = Message("Verification email", sender=("adaptxchange@gmail.com"), recipients=[email])
    msg.body = "Here is some verification stuff"
    msg.html = html
    try:
        mail.send(msg)
    except Exception:
        flash("Error sending email, please try and accept again")
        return redirect("/admin")

    flash ("Successfully sent email")
    teamDB.acceptTeam(teamName)    

    return redirect("/")


@admin.route('/confirm/<token>')
def confirmEmail(token):
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)

    team = teamDB.getTeamByEmail(email)

    teamDB.setEmailVerified(team["teamName"])

    flash("Successfully confirmed")

    return redirect(url_for('home.login'))


@admin.route("/admin/rejectTeam/<teamName>")
def rejectTeam(teamName):
    if current_user.isAdmin != True:
        flash("You are not permitted to do this")
        return redirect(url_for("home.index"))

    teamDB.removeTeam(teamName)
    return redirect(url_for("admin.adminPanel"))

