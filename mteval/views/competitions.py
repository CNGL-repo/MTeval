from mteval import app
from flask import Blueprint, Flask, render_template, request, send_file, redirect, url_for, Response, flash, send_from_directory
from flask.ext.login import request, current_user, LoginManager, logout_user, login_required
from mteval.forms import LoginForm, RegisterForm, EditTeamForm, CompetitionForm, CompetitionEditForm
from mteval.database import teamDB, compDB
from werkzeug import secure_filename
import os


competitions = Blueprint("competitions", __name__)


#Competition routes
@competitions.route("/")
def competitions_home():
    comps = compDB.getCompList()
    return render_template("competitions/competitions.html", comps=comps)

@competitions.route("/addCompetition/", methods=["GET", "POST"])
@login_required
def addCompetition():
    if current_user.isAdmin == False:
        flash("You are not an admin")
        return redirect(url_for("competitions.competitions_home"))

    form = CompetitionForm(request.form)
    if request.method == "POST" and form.validate():
        testData = request.files["testData"]
        trainingData = request.files["trainingData"]

        ##TODO: CHANGE NAMING
        #overwrites duplicate names
        testDataName = secure_filename(testData.filename)
        trainingDataName = secure_filename(trainingData.filename)
        if testDataName != "":
            testData.save(os.path.join(app.config["UPLOAD_DIR"], testDataName))
        if trainingDataName != "":
            trainingData.save(os.path.join(app.config["UPLOAD_DIR"], trainingDataName))
        
        res = compDB.addComp( 
            form.name.data,
            form.description.data,
            form.deadline.data,
            form.submissionFormat.data,
            form.requirements.data,
            form.organisers.data,
            form.contact.data,
            testDataName,
            trainingDataName
        )

        return redirect(url_for("competitions.competitions_home"))

    return render_template("competitions/addCompetition.html", form=form, formAction="/comps/addCompetition/")

@competitions.route("/editCompetition/<name>", methods=["GET", "POST"])
@login_required
def editCompetition(name):
    if current_user.isAdmin == False:
        flash("You are not an admin")
        return redirect(url_for("competitions_home"))    
    form = CompetitionEditForm(request.form)
    if request.method == "POST" and form.validate():
        testData = request.files["testData"]
        trainingData = request.files["trainingData"]

        ##TODO: CHANGE NAMING
        #overwrites duplicate names
        testDataName = secure_filename(testData.filename)
        trainingDataName = secure_filename(trainingData.filename)
        if testDataName != "":
            testData.save(os.path.join(app.config["UPLOAD_DIR"], testDataName))
        if trainingDataName != "":
            trainingData.save(os.path.join(app.config["UPLOAD_DIR"], trainingDataName))
        
        res = compDB.editComp( 
            name,
            form.name.data,
            form.description.data,
            form.deadline.data,
            form.submissionFormat.data,
            form.requirements.data,
            form.organisers.data,
            form.contact.data,
            testDataName,
            trainingDataName
        )

        return redirect(url_for("competitions.competitions_home"))

    comp = compDB.getCompByName(name)
    form.name.data = comp["compName"]
    form.description.data = comp["description"]
    form.deadline.data = comp["deadline"]
    form.submissionFormat.data = comp["format"]
    form.requirements.data = comp["requirements"]
    form.organisers.data = comp["organisers"]
    form.contact.data = comp["contact"]

    return render_template("competitions/addCompetition.html", form=form, formAction="/comps/editCompetition/{0}".format(name))

@competitions.route("/removeCompetition/<name>")
@login_required
def removeCompetition(name):    
    if current_user.isAdmin == False:
        flash("You are not an admin")
        return redirect(url_for("competitions.competitions_home"))

    compDB.removeComp(name)

    return redirect(url_for("competitions.competitions_home"))

@competitions.route("/download/<name>")
@login_required
def downloadFile(name):
    return send_from_directory(app.config["UPLOAD_DIR"], name)

@competitions.route("/upload", methods = ["GET", "POST"])
@login_required
def uploadSubmission():
    if request.method == "POST":
        subData = request.files["file"]
        compId = request.form.get("compId")
        teamId = request.form.get("teamId")    
        subDataName = secure_filename(subData.filename)
        if subDataName != "":
            subData.save(os.path.join(app.config["UPLOAD_DIR"], subDataName))
    return redirect("/")        
        