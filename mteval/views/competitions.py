from mteval import app, celery, converters
from flask import Blueprint, Flask, render_template, request, send_file, redirect, url_for, Response, flash, send_from_directory
from flask.ext.login import request, current_user, LoginManager, logout_user, login_required
from mteval.forms import LoginForm, RegisterForm, EditTeamForm, CompetitionForm, CompetitionEditForm
from mteval.database import teamDB, compDB
from mteval.decorators import async
from werkzeug import secure_filename
import os
import time

#blueprint for competitions
#prefix: "/comps"
competitions = Blueprint("competitions", __name__)


#Competition routes
@competitions.route("/")
def competitions_home():
    comps = compDB.getCompList()
    return render_template("competitions/competitions.html", comps=comps)

#Add a competition
#GET request renders a template with a form to add competitions
#POST request takes form information and adds a database entry for the competition
@competitions.route("/addCompetition/", methods=["GET", "POST"])
@login_required
def addCompetition():
    #Only admins should be allowed to add a competition
    if current_user.isAdmin == False:
        flash("You are not an admin")
        return redirect(url_for("competitions.competitions_home"))

    #Form as defined in forms.py
    form = CompetitionForm(request.form)
    if request.method == "POST" and form.validate():
        #Get the files uploaded by the admin as part of the competition
        testData = request.files["testData"]
        trainingData = request.files["trainingData"]

        #Clean the names given by the user
        testDataName = secure_filename(testData.filename)
        trainingDataName = secure_filename(trainingData.filename)
        
        #Save the files
        if testDataName != "":
            testData.save(os.path.join(app.config["UPLOAD_DIR"], testDataName))
        if trainingDataName != "":
            trainingData.save(os.path.join(app.config["UPLOAD_DIR"], trainingDataName))
        
        #Add entry in database
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

    #FormAction is passed to the template so it can change the action of the submit button based on whether a competition
    #is being edited or added
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
        compName = request.form.get("compName")
        teamName = request.form.get("teamName")    
        
        if not allowedFile(subData.filename):
            flash("File type not accepted")
            return redirect("/comps")

        subDataName = secure_filename("{0}-{1}-{2}".format(compName, teamName, int(time.time())))
        filePath = os.path.join(app.config["UPLOAD_DIR"], subDataName)
        if subDataName != "":
            try:
                subData.save(filePath)
            except Exception:
                flash("Error saving file, please try to upload again")
                return redirect("/comps")

        teamDB.appendSub(subDataName, teamName, compName)

    convertToCsv(filePath)

    flash("File uploaded")
    return redirect("/")        
    

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config["ALLOWED_EXTENSIONS"]
@async
def convertToCsv(filename):
    converters.SGMLToCSVW(filename)
