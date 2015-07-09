from flask import Flask
from flask_bootstrap import Bootstrap

app = Flask(__name__, static_url_path="/static")
app.config.from_pyfile("config.cfg")
Bootstrap(app)



import mteval.routes
