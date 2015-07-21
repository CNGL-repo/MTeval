from mteval import app

from flask import render_template, flash, redirect, url_for, request
from flask.ext.login import request, current_user, LoginManager, logout_user, login_required
from forms import LoginForm, RegisterForm, EditTeamForm, CompetitionForm
from database import teamDB, compDB
import loginUtils
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Mail, Message
from urlparse import urlparse, urljoin
from werkzeug import secure_filename
import os


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
        emailVerified = True, 
        isActive = True)

#Application routes
@app.route('/')
def index():
    upcomingComps = compDB.getUpcomingCompList()
    return render_template("index.html", upcomingComps=upcomingComps)

#Route for admin panel, where the admin can do various tasks
@app.route('/admin')
@login_required
def adminPanel():
    if current_user.isAdmin != True:
        flash("You are not an admin")
        return redirect(url_for("index"))

    #perhaps it might be better to get all teams once and then check for conditions in template?
    #rather than querying twice and passing a lot of redundant information 
    pendingTeams = teamDB.getPendingTeams()
    teams = teamDB.getTeamList()
    return render_template("adminPanel.html", pendingTeams=pendingTeams, teams=teams)


###Login & registration routes
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

    return render_template("register.html", form = form)

@app.route("/acceptTeam/<teamName>")
def acceptTeam(teamName):
    if current_user.isAdmin != True:
        flash("You are not permitted to do this")
        return redirect(url_for("index"))

    teamDB.acceptTeam(teamName)
    return redirect(url_for("adminPanel"))

@app.route("/rejectTeam/<teamName>")
def rejectTeam(teamName):
    if current_user.isAdmin != True:
        flash("You are not permitted to do this")
        return redirect(url_for("index"))

    teamDB.removeTeam(teamName)
    return redirect(url_for("adminPanel"))

@app.route("/editTeam/<teamName>", methods=["GET", "POST"])
def editTeam(teamName):
    #only the current team may edit itself, or the admin may edit every team
    if current_user.isAdmin != True and current_user.teamName != teamName:
        flash("You don't have permission to edit this team")
        return redirect(url_for("index"))

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
        return redirect(url_for("index"))

    team = teamDB.getTeamByName(teamName)
    return render_template("editTeam.html", team=team, form=form)

#Competition routes
@app.route("/competitions")
def competitions():
    comps = compDB.getCompList()
    return render_template("competitions.html", comps=comps)

@app.route("/addCompetition", methods=["GET", "POST"])
def addCompetition():
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

        return redirect(url_for("competitions"))

    return render_template("addCompetition.html", form=form)

@lm.user_loader
def load_user(userId):
    return loginUtils.getTeamObject(userId)

@lm.unauthorized_handler
def showLoginPage():
    return redirect(url_for("login"))

##UTILS
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

def safeRedirect(endpoint="index", **values):
    next = request.args.get("next")
    if is_safe_url(next):
        return redirect(next)
    target = get_redirect_target()
    return redirect(target or url_for(endpoint, **values))