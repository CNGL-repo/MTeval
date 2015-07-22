from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager

app = Flask(__name__, static_url_path="/static")
app.config.from_pyfile("config.cfg")
Bootstrap(app)

#Login manager initialisation
lm = LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(userId):
    return loginUtils.getTeamObject(userId)

@lm.unauthorized_handler
def showLoginPage():
    return redirect(url_for("home.login"))

from .views.home import home
from .views.admin import admin
from .views.competitions import competitions
from .views.teams import teams

app.register_blueprint(home)
app.register_blueprint(admin)
app.register_blueprint(competitions, url_prefix="/comps")
app.register_blueprint(teams, url_prefix="/teams")

