from flask import Flask, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cxYFqST8YcuK6wZV6Aoy-P_JBVYXBMSUlLBV2WsCKWQ'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://lynko:lynko@localhost/academy'

import models.multiquestion as Multi

@app.route("/api/ping")
def ping():
    answer = {}
    answer = { "status": "pong", }
    return jsonify(message=answer)

@app.route("/api/multiquestions", methods=['GET'])
def get_multiquestions():
    list_questions = Multi.Questions.query.all()

    return jsonify(multiquestions=[Multi.Questions.serialize(question) for question in list_questions])



if __name__ == "__main__":
    app.run(debug=True)
