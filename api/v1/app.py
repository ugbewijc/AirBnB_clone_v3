#!/usr/bin/python3
"""
Create API endpoint in flask
"""


from flask import Flask, jsonify, make_response
from models import storage
from os import getenv
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(obj):
    """
    Close storage
    """
    storage.close()


@app.errorhandler(404)
def not_found_route(e):
    """
    Custom 404 page
    """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":

    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default=5000)

    app.run(host, int(port), threaded=True)
