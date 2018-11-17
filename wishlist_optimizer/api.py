import logging

from flask import Blueprint, jsonify, request
from wishlist_optimizer.wishlist_service import WishlistService
from wishlist_optimizer.languages_service import LanguagesService
from wishlist_optimizer.jobs import check_job_status, schedule_job, get_pricing
from wishlist_optimizer.auth import login_required


api = Blueprint('api', __name__)
languages_service = LanguagesService()
wishlist_service = WishlistService(languages_service)

logger = logging.getLogger(__name__)


@api.route('/wishlists', methods=('GET', 'POST'))
@login_required
def get_wishlists(user_id):
    if request.method == 'GET':
        return jsonify({'wishlists': wishlist_service.get_wishlists(user_id)})
    return jsonify(
        {
            'wishlist': wishlist_service.create_wishlist(
                user_id, request.get_json()
            )
         }
    ), 201


@api.route('/wishlists/<int:wishlist_id>', methods=('GET',))
@login_required
def get_wishlist(user_id, wishlist_id):
    return jsonify(
        {'wishlist': wishlist_service.get_wishlist(user_id, wishlist_id)}
    )


@api.route('/wishlists/<int:wishlist_id>', methods=('DELETE',))
@login_required
def delete_wishlist(user_id, wishlist_id):
    wishlist_service.remove_wishlist(user_id, wishlist_id)
    return ('', 204)


@api.route('/wishlists/<int:wishlist_id>/cards', methods=('GET', 'POST'))
@login_required
def get_cards(user_id, wishlist_id):
    if request.method == 'GET':
        return jsonify(
            {
                'cards': wishlist_service.get_wishlist(
                    user_id, wishlist_id
                )['cards']
             }
        )
    data = request.get_json()
    return jsonify(
        {'card': wishlist_service.add_card(user_id, wishlist_id, data)}
    ), 201


@api.route('/wishlists/<int:wishlist_id>/cards/<int:card_id>', methods=['DELETE',])  # noqa
@login_required
def delete_card(user_id, wishlist_id, card_id):
    wishlist_service.remove_card(user_id, card_id)
    return '', 204


@api.route('/wishlists/<int:wishlist_id>/cards/<int:card_id>', methods=['PUT',])  # noqa
@login_required
def update_card(user_id, wishlist_id, card_id):
    return jsonify(
        {
            'card': wishlist_service.update_card(
                user_id, card_id, request.get_json()
            )
         }
    )


@api.route('/pricing', methods=('POST', ))
def submit_pricing_job():
    wishlist = request.get_json().get('wishlist')
    if not wishlist:
        return jsonify({'error': 'wishlist is missing'}), 400
    job_result = schedule_job(get_pricing, wishlist)
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


@api.route('/languages', methods=('GET',))
def get_languages():
    return jsonify(languages_service.get_all_languages())
