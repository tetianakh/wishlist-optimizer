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
        'grant_type': 'authorization_code',
    }

    resp = requests.post(url, data=data, headers=headers)
    resp_data = resp.json()
    if 'error' in resp_data:
        return jsonify(resp_data), 400
    jwt_token = resp_data['id_token']
    refresh_token = resp_data.get('refresh_token')
    user_id = user_service.validate_token(jwt_token)
    if refresh_token:
        # refresh token is sent only during 1st login
        user_service.save_refresh_token(user_id, refresh_token)
    return jsonify({'token': jwt_token})


def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({'error': 'Authorization header is missing'}), 401
        jwt_token = request.headers['Authorization'].replace('Bearer ', '')
        try:
            user_id = user_service.validate_token(jwt_token)
        except TokenValidationError:
            return jsonify({'error': 'Invalid auth token'}), 401
        try:
            return view(user_id, *args, **kwargs)
        except ObjectNotFound:
            return 'Object not found', 404

    return inner


@auth.route('/refresh', methods=['POST'])
def refresh():
    try:
        token = request.headers['Authorization'].replace('Bearer ', '')
    except KeyError:
        return 'Missing auth header', 401
    user_id, refresh_token = user_service.get_refresh_token(token)
    if not refresh_token:
        return 'Failed to get refresh token', 401
    data = {
        'client_id': current_app.config['GOOGLE_CLIENT_ID'],
        'client_secret': current_app.config['GOOGLE_CLIENT_SECRET'],
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    url = 'https://www.googleapis.com/oauth2/v4/token'
    resp = requests.post(url, data=data, headers=headers)
    try:
        return jsonify({'token': resp.json()['id_token']}), 200
    except Exception as e:
        logger.exception('Failed to refresh token for user %s: %s', user_id, e)
        user_service.invalidate_token(user_id)
        return 'Failed to get a new jwt token', 401
