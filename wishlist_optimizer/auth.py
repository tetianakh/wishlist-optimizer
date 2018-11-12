import logging

import cachecontrol
from google.oauth2 import id_token
import google.auth.transport.requests
import requests
from flask import Blueprint, request, jsonify, current_app

from wishlist_optimizer.user_service import UserService

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
