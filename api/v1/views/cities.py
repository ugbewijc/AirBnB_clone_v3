#!/usr/bin/python3


"""
Default RESTFul API endpoint that handels Sate objects
Routes:
    /states/<state_id>/cities: GET - Retrieves  all City objects of a State
                               POST - Creates a City
    /cities/<city_id>: GET - Retrieves a City object
                        DELETE - Deletes a City object
                        PUT - Updates a State object
"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities_in_a_state_route(state_id):
    """
    Retrive all cities in a state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = [obj.to_dict() for obj in state.cities]
    return jsonify(all_cities)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                  strict_slashes=False)
def city_route(city_id):
    """
    Retrive city object by City ID
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_route(city_id):
    """
    Delete city by City ID
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city_route(state_id):
    """
    Create new City
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    city_js = request.get_json()
    obj = City(**city_js)
    obj.state_id = state.id
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city_route(city_id):
    """
    Update a city object
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
