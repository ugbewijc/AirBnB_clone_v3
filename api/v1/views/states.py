#!/usr/bin/python3


"""
Default RESTFul API endpoint that handels Sate objects
Routes:
    /states: GET - Retrieves the list of all State objects
             POST - Creates a State
    /states/<state_id>: GET - Retrieves a State object
                        DELETE - Deletes a State object
                        PUT - Updates a State object
"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states_route():
    """
    Retrive all states
    """
    all_states = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(all_states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def a_state_route(state_id):
    """
    Retrive states by State ID
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_route(state_id):
    """
    Delete state by State ID
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def create_state_route():
    """
    Create new State Obj
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    request_js = request.get_json()
    obj = State(**request_js)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state_route(state_id):
    """
    Update a State Details
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
