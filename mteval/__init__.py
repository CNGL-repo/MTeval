from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager
from celery import Celery

app = Flask(__name__, static_url_path="/static")
app.config.from_pyfile("config.cfg")
Bootstrap(app)

#Login manager initialisation
lm = LoginManager()
lm.init_app(app)

def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

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

