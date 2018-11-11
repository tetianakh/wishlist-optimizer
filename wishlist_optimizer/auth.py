import logging

import requests
from flask import Blueprint, request, jsonify, current_app

auth = Blueprint('auth', __name__)
logger = logging.getLogger(__name__)


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
        'redirect_uri': 'http://localhost:5000',
        'grant_type': 'authorization_code'
    }

    resp = requests.post(url, data=data, headers=headers)
    logger.info('Google response: %s', resp.text)
    resp_data = resp.json()
    if 'error' in resp_data:
        return resp_data['error'], 401
    return jsonify({'token': resp_data['id_token']})


@auth.route('/google-redirect', methods=['POST'])
def complete_google_auth():
    logger.info(request.get_json())
    return '', 200
