#!/usr/bin/python3


"""
Status Route module
Routes:
    /status
    /stats: retrieves the number of each objects by type
"""


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status_route():
    """
    Return status = ok in json format
    """
    return jsonify(status="OK")


@app_views.route('/stats', strict_slashes=False)
def stats_route():
    """
    Return number of each object by type
    """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
