from mteval import app, loginUtils
from flask import Blueprint, Flask, render_template, request, send_file, redirect, url_for, Response, flash
from flask.ext.login import request, current_user, LoginManager, logout_user, login_required
from mteval.forms import LoginForm, RegisterForm, EditTeamForm, CompetitionForm, CompetitionEditForm
from mteval.database import teamDB, compDB


teams = Blueprint("teams", __name__)

@teams.route("/editTeam/<teamName>", methods=["GET", "POST"])
def editTeam(teamName):
    #only the current team may edit itself, or the admin may edit every team
    if current_user.isAdmin != True and current_user.teamName != teamName:
        flash("You don't have permission to edit this team")
        return redirect(url_for("home.index"))

    form = EditTeamForm(request.form)
    if request.method == "POST" and form.validate():
        teamDB.editTeam(
            teamName,
            form.teamname.data, 
            form.email.data,
            form.organisation.data,
            loginUtils.hashPassword(form.password.data)
        )
        flash("Updated team successfully")
        return redirect(url_for("home.index"))

    team = teamDB.getTeamByName(teamName)
    form.teamname.data = team["teamName"]
    form.email.data = team["email"]
    form.organisation.data = team["organisation"]
    return render_template("teams/editTeam.html", team=team, form=form)

