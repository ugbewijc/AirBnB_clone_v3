#!/usr/bin/python3


"""
RESTFul API endpoint that handels Place objects
Routes:
    /cities/<city_id>/places: GET - Retrieves the list of all Place objects
                              POST - Creates a Place
    /places/<place_id>: GET - Retrieves a Place object
                        DELETE - Deletes a Users object
                        PUT - Updates a Users object
"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_places_in_a_city_route(city_id):
    """
    Retrive all Places in a City
    """
    city = storage.get("City", city_id)
    if all_city is None:
        abort(404)
    all_places = [p.to_dict() for p in city.places]
    return jsonify(all_places), 200


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_route(place_id):
    """
    Retrive place object by place ID
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_route(place_id):
    """
    Delete place by place ID
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place_route(city_id):
    """
    Create new place
    """
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    elif "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    else:
        obj_data = request.get_json()
        city = storage.get("City", city_id)
        user = storage.get("User", obj_data['user_id'])
        if city is None or user is None:
            abort(404)
        obj_data['city_id'] = city.id
        obj_data['user_id'] = user.id
        obj = Place(**obj_data)
        obj.save()
        return jsonify(obj.to_dict()), 201
