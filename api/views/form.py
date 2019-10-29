from api import app
from flask import render_template, request
from random import shuffle
from api.models import multiquestion as Multi

# Full path for the URL
URL_VERSION = app.config["URL_VERSION"]

# Route created just to be able to debug while FrontEnd is not done.
@app.route(f"{URL_VERSION}/form", methods=["GET", "POST"])
def form():
    if request.method == "GET":
        opt = [i for i in range(1,5)]
        shuffle(opt)
        options = {
            opt[0] : "Right Answer",
            opt[1] : "Option 1",
            opt[2] : "Option 2",
            opt[3] : "Option 3"
        }
        correct = "opt" + str(list(options.items())[0][0])
        qtype = Multi.Types.query.distinct(Multi.Types.type).all()
        return render_template("form.html", options = options, correct = correct, qtype = qtype)