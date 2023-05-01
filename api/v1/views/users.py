#!/usr/bin/python3


"""
RESTFul API endpoint that handels Users objects
Routes:
    /users: GET - Retrieves the list of all Users objects
             POST - Creates a Users
    /users/<users_id>: GET - Retrieves a Users object
                       DELETE - Deletes a Users object
                       PUT - Updates a Users object
"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users_route():
    """
    Retrive all users
    """
    all_users = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(all_users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def user_route(user_id):
    """
    Retrive user by users ID
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_route(user_id):
    """
    Delete user by users ID
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
def create_user_route():
    """
    Create new User
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password'not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    user_js = request.get_json()
    obj = User(**user_js)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user_route(user_id):
    """
    Update User Object
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'email', 'created_at', 'updated']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
