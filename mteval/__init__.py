from flask import Flask
from flask_bootstrap import Bootstrap
from flask.ext.login import LoginManager

app = Flask(__name__, static_url_path="/static")
app.config.from_pyfile("config.cfg")
Bootstrap(app)

lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"

import mteval.routes
