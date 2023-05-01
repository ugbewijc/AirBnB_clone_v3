#!/usr/bin/python3


"""
RESTFul API endpoint that handels Amenities objects
Routes:
    /amenities: GET - Retrieves the list of all Amenity objects
                POST - Creates a Amenity
    /amenities/<amenity_id>: GET - Retrieves a Amenity object
                             DELETE - Deletes a Amenity object
                             PUT - Updates a Amenity object
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_route():
    """
    Retrive all amenities
    """
    all_amenities = [obj.to_dict() for obj in storage.all(Amenity).values()]
    return jsonify(all_amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_route(amenity_id):
    """
    Retrive amenity by Amenity ID
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_route(amenity_id):
    """
    Delete amenity by amenity ID
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def create_obj_amenity():
    """
    Create new Amenity
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    amenities_js = request.get_json()
    obj = Amenity(**amenities_js)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def post_amenity(amenity_id):
    """
    Update Amenity object
    """
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict())
