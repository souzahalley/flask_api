from flask import Flask

app = Flask(__name__)

app.config.from_object("config.Config")

# DEBUG
from api.views import ping
from api.views import form

# Questions
from api.views import multiquestions
