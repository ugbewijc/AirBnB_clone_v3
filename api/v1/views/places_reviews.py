#!/usr/bin/python3


"""
RESTFul API endpoint that handels Reviews objects
Routes:
    /places/<place_id>/reviews: GET - Retrieves all Review objects
                                POST - Creates a Review
    /reviews/<review_id>: GET - Retrieves a Review object
                          DELETE - Deletes a Review object
                          PUT - Updates a Review object
"""


from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_review_by_place_route(place_id):
    """
    Retrive reviews in a place
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    all_review = [obj.to_dict() for obj in place.reviews]
    return jsonify(all_review), 200


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def review_route(review_id):
    """
    Retrive Review by Review ID
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_route(review_id):
    """
    Delete review by Review ID
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """
    Create new review
    """
    if storage.get("Place", place_id) is None:
        abort(404)
    elif not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "user_id" not in request.get_json():
        return jsonify({"error": "Missing user_id"}), 400
    elif storage.get("User", request.get_json()["user_id"]) is None:
        abort(404)
    elif "text" not in request.get_json():
        return jsonify({"error": "Missing text"}), 400
    else:
        obj_data = request.get_json()
        obj = Review(**obj_data)
        obj.place_id = place_id
        obj.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Update review by Review ID
    """
    obj = storage.get("Review", review_id)
    if obj is None:
        abort(404)
    elif not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    else:
        obj_data = request.get_json()
        ignore = ("id", "user_id", "place_id", "created_at", "updated_at")
        for k in obj_data.keys():
            if k in ignore:
                pass
            else:
                setattr(obj, k, obj_data[k])
        obj.save()
        return jsonify(obj.to_dict()), 200
