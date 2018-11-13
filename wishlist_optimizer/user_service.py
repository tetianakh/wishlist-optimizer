import logging
from wishlist_optimizer.models import User, db, RevokedToken

import cachecontrol
import requests
from google.oauth2 import id_token
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
            r = google.auth.transport.requests.Request(session=self._session)
            id_info = id_token.verify_oauth2_token(
                jwt_token, r, current_app.config['GOOGLE_CLIENT_ID']
            )
            logger.debug(id_info)
            if id_info['iss'] != current_app.config['GOOGLE_ISS']:
                raise ValueError('Wrong issuer.')

            user_sub = id_info['sub']
        except Exception as e:
            raise TokenValidationError() from e
        logger.info(user_sub)
        return self.get_or_create_user(user_sub)

    @staticmethod
    def get_or_create_user(user_sub):
        user = User.query.filter_by(sub=user_sub).first()
        if not user:
            user = User(sub=user_sub)
            db.session.add(user)
            db.session.commit()
        return user.id

    def revoke(self, jwt_token):
        token = RevokedToken(jwt=jwt_token)
        db.session.add(token)
        db.session.commit()

    def save_refresh_token(self, user_id, refresh_token):
        user = User.query.get(user_id)
        user.refresh_token = refresh_token
        db.session.commit()
