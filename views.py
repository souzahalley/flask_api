from flask import Flask, jsonify, request, make_response, render_template
from random import shuffle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cxYFqST8YcuK6wZV6Aoy-P_JBVYXBMSUlLBV2WsCKWQ'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://lynko:lynko@localhost/academy'

import models.multiquestion as Multi

# Full path for the URL
URL_VERSION = "/api/v1"

# Just to check the availability of the WSGI
@app.route(f"{URL_VERSION}/ping", methods=['GET'])
def ping():
    answer = {}
    answer['status'] = 'pong'
    return make_response(jsonify(message=answer), 200)

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

# Route responsible for listing all multiquestions (GET) 
# and also for adding new ones.
# TODO: Create filter when listing. By TAG and also by TYPE, or both at same

@app.route(f"{URL_VERSION}/multiquestions", methods=['GET', 'POST'])
def multiquestion():
    if request.method == "GET":
        query_all = Multi.Questions.query.all()
        return jsonify(multiquestion=[Multi.Questions.serialize(q) for q in query_all])

    elif request.method == "POST":
        res = request.form

        question = Multi.Questions(
            correct = res.get("correct"),
            option1 = res.get("opt1"),
            option2 = res.get("opt2"),
            option3 = res.get("opt3"),
            option4 = res.get("opt4"),
            question = res.get("question"),
            score = res.get("score")
        )

        tags = res.get("tags").split(" ")

        for tag in tags:
            t = tag.lower()

            # Validate if tag exist on the database
            check = Multi.Tags.query.filter(Multi.Tags.tagname==t).first()

            if check:
                # TODO: Need to validate how to add new relationship to an existing value on the table
                # OBS: I dont want duplicate tags in the same table, please think
                pass
            else:
                add_tag = Multi.Tags(tagname=t, question=[question])
                Multi.db.session.add(add_tag)
                

        types = {}
        qtype = Multi.Types.query.distinct(Multi.Types.type).all()
        for q in qtype:
            typename = res.get(q.type)
            add_type = Multi.Types(type=q.type, typename=typename, question=[question])
            types[q.type] = typename
            Multi.db.session.add(add_type)
        
        if Multi.db.session.commit():
            return make_response(jsonify(question, types, tags), 200)
        else:
            answer = {}
            answer['status'] = 'Format Error'
            return make_response(jsonify(message=answer), 400)


if __name__ == "__main__":
    app.run(debug=True)
