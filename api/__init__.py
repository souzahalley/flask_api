from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_praetorian import Praetorian

app = Flask(__name__)
app.config.from_object("config.Config")
db = SQLAlchemy(app)
guard = Praetorian()

# DEBUG
from api.views import ping
from api.views import form

# Questions
from api.views import multiquestions

# Login
from api.views import login
