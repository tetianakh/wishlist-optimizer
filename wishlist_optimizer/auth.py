import logging
from functools import wraps

import requests
from flask import Blueprint, request, jsonify, current_app

from wishlist_optimizer.user_service import UserService, TokenValidationError
from wishlist_optimizer.wishlist_service import ObjectNotFound

auth = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


user_service = UserService()


@auth.route('/google', methods=['POST'])
def log_in_with_google():
    request_data = request.get_json()
    logger.info('Response: `%s`, `%s`', request.args, request_data)
    if 'code' not in request_data or 'error' in request_data:
        return jsonify(request_data), 401
    client_id = current_app.config['GOOGLE_CLIENT_ID']
    client_secret = current_app.config['GOOGLE_CLIENT_SECRET']
    url = 'https://www.googleapis.com/oauth2/v4/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'code': request_data['code'],
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': current_app.config['GOOGLE_REDIRECT_URL'],
        'grant_type': 'authorization_code'
    }

    resp = requests.post(url, data=data, headers=headers)
    logger.info('Google response: %s', resp.text)
    resp_data = resp.json()
    if 'error' in resp_data:
        return resp_data['error'], 401
    jwt_token = resp_data['id_token']
    user_service.validate_token(jwt_token)
    return jsonify({'token': jwt_token})


@auth.route('/logout', methods=['POST'])
def logout():
    user_service.revoke(request.get_json()['token'])
    return 'Token has been revoked', 200


def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        jwt_token = request.headers['Authorization']
        try:
            user_id = user_service.validate_token(jwt_token)
        except TokenValidationError:
            return jsonify({'error': 'Invalid auth token'}), 401
        try:
            return view(user_id, *args, **kwargs)
        except ObjectNotFound:
            return 'Object not found', 404

    return inner
