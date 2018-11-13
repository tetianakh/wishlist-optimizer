from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Wishlist(db.Model):
    __tablename__ = 'wishlist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cards = db.relationship(
        'Card', backref="wishlist", lazy=False, cascade="all, delete-orphan"
    )
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            cards=[card.to_dict() for card in self.cards]
        )


cards_to_languages = db.Table('cards_to_languages',
    db.Column('card_id', db.Integer, db.ForeignKey('card.id'), primary_key=True),  # noqa
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'), primary_key=True)  # noqa
)


class Card(db.Model):
    __tablename__ = 'card'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, default=lambda: 1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlist.id'))
    languages = db.relationship(
        'Language', secondary=cards_to_languages, lazy='subquery',
        backref=db.backref('cards', lazy=True)
    )

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            quantity=self.quantity,
            languages=[l.name for l in self.languages]
        )


class Language(db.Model):
    __tablename__ = 'language'
    __table_args__ = (
        db.UniqueConstraint('name', 'mkm_id', name='unique_name_mkm_id'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    mkm_id = db.Column(db.Integer, nullable=False)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sub = db.Column(db.Text, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    refresh_token = db.Column(db.String(128))
    wishlists = db.relationship(
        'Wishlist', backref="user", lazy=False, cascade="all, delete-orphan"
    )


class RevokedToken(db.Model):
    __tablename__ = 'revoked_token'
    id = db.Column(db.Integer, primary_key=True)
    jwt = db.Column(db.String(2000))
