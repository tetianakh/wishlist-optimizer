import logging
from wishlist_optimizer.models import User, db, RevokedToken

import cachecontrol
import requests
from google.oauth2 import id_token
from google.auth import jwt
import google.auth.transport.requests
from flask import current_app


logger = logging.getLogger(__name__)


class TokenValidationError(ValueError):
    pass


class UserService:
    def __init__(self):
        session = requests.session()
        self._session = cachecontrol.CacheControl(session)

    def validate_token(self, jwt_token):
        if RevokedToken.query.filter_by(jwt=jwt_token).first():
            raise TokenValidationError()
        try:
            id_info = self._get_id_info(jwt_token)
            if id_info['iss'] != current_app.config['GOOGLE_ISS']:
                raise ValueError('Wrong issuer.')

            user_sub = id_info['sub']
        except Exception as e:
            raise TokenValidationError() from e
        return self._get_or_create_user(user_sub)

    @staticmethod
    def _get_or_create_user(user_sub):
        user = User.query.filter_by(sub=user_sub).first()
        if not user:
            user = User(sub=user_sub)
            db.session.add(user)
            db.session.commit()
        logger.debug('User: %s', user)
        return user.id

    def revoke(self, jwt_token):
        token = RevokedToken(jwt=jwt_token)
        db.session.add(token)
        db.session.commit()

    def save_refresh_token(self, user_id, refresh_token):
        user = User.query.get(user_id)
        if not user:
            logger.warning(
                'No user found for id %s, cannot save refresh token', user_id
            )
            return
        user.refresh_token = refresh_token
        logger.info('Saving refresh token for user %s', user)
        db.session.add(user)
        db.session.commit()

    def get_refresh_token(self, jwt_token):
        try:
            decoded = jwt.decode(jwt_token, verify=False)
        except ValueError:
            return None
        logger.info('Decoded token: %s', decoded)
        if 'sub' not in decoded:
            return None
        user = User.query.filter_by(sub=decoded['sub']).first()
        logger.info(User.query.all())
        return user.refresh_token if user else None

    def _get_id_info(self, jwt_token):
        r = google.auth.transport.requests.Request(session=self._session)
        return id_token.verify_oauth2_token(
            jwt_token, r, current_app.config['GOOGLE_CLIENT_ID']
        )
