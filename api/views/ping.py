from api import app
from flask import make_response, jsonify

# Full path for the URL
URL_VERSION = app.config["URL_VERSION"]

# Just to check the availability of the WSGI
@app.route(f"{URL_VERSION}/ping", methods=['GET'])
def ping():
    answer = {}
    answer['status'] = 'pong'
    return make_response(jsonify(message=answer), 200)