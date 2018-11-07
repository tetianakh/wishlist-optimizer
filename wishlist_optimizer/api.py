import logging

from flask import Blueprint, jsonify, request
from wishlist_optimizer.wishlist_service import WishlistService
from wishlist_optimizer.jobs import check_job_status, schedule_job, get_pricing

api = Blueprint('api', __name__)
wishlist_service = WishlistService()
logger = logging.getLogger(__name__)


@api.route('/wishlists', methods=('GET', 'POST'))
def get_wishlists():
    if request.method == 'GET':
        return jsonify({'wishlists': wishlist_service.get_wishlists()})
    return jsonify(
        {'wishlist': wishlist_service.create_wishlist(request.get_json())}
    ), 201


@api.route('/wishlists/<int:wishlist_id>', methods=('GET',))
def get_wishlist(wishlist_id):
    return jsonify(
        {'wishlist': wishlist_service.get_wishlist(wishlist_id)}
    )


@api.route('/wishlists/<int:wishlist_id>/cards', methods=('GET', 'POST'))
def get_cards(wishlist_id):
    if request.method == 'GET':
        return jsonify(
            {'cards': wishlist_service.get_wishlist(wishlist_id)['cards']}
        )
    data = request.get_json()
    return jsonify(
        {'card': wishlist_service.add_card(wishlist_id, data)}
    ), 201

@api.route('/wishlists/<int:wishlist_id>/cards/<int:card_id>', methods=['DELETE',])  # noqa
def delete_card(wishlist_id, card_id):
    wishlist_service.remove_card(card_id)
    return '', 204


@api.route('/wishlists/<int:wishlist_id>/cards/<int:card_id>', methods=['PUT',])  # noqa
def update_card(wishlist_id, card_id):
    return jsonify(
        {'card': wishlist_service.update_card(card_id, request.get_json())}
    )


@api.route('/pricing', methods=('POST', ))
def submit_pricing_job():
    wishlist_id = request.get_json().get('wishlist_id')
    if not wishlist_id:
        return jsonify({'error': 'wishlist id is missing'}), 400
    job_result = schedule_job(
        get_pricing, wishlist_service.get_wishlist(wishlist_id)
    )
    if job_result:
        return jsonify(job_result), 202
    return jsonify({'error': 'failed to submit pricing calculation job'}), 400


@api.route('/pricing/<string:job_id>', methods=('GET', ))  # noqa
def get_pricing_job_status(job_id):
    job_result = check_job_status(job_id)
    if job_result:
        return jsonify(job_result)
    return jsonify(
        {'error': 'failed to fetch pricing calculation job status'}
    ), 404
