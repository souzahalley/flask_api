from api import app, guard
from flask import jsonify, request, make_response
from flask_praetorian import auth_required, roles_required
from datetime import datetime

import api.models.login as Login

# guard.init_app(app, Login.Users)

# Full path for the URL
URL_VERSION = app.config["URL_VERSION"]

@app.route(f"{URL_VERSION}/users", methods=['GET'])
@roles_required('admin')
def users():
    query = Login.Users.query.all()
    return jsonify([Login.Users.serialize(q) for q in query])

@app.route(f"{URL_VERSION}/login", methods=['POST'])
def login():
    res = request.get_json(force=True)
    username = res.get('username', None)
    password = res.get('password', None)

    # Validate
    valid = guard.authenticate(username, password)

    # If authenticate
    valid.last_login = datetime.utcnow()
    Login.db.session.commit()

    answer = {'access_token' : guard.encode_jwt_token(valid)}
    return jsonify(answer)