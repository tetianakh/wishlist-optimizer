from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Wishlist(db.Model):
    __tablename__ = 'wishlist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    cards = db.relationship(
        'Card', backref="wishlist", lazy=False, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            created_at=self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            cards=[card.to_dict() for card in self.cards]
        )


class Card(db.Model):
    __tablename__ = 'card'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    quantity = db.Column(db.Integer, default=lambda: 1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlist.id'))

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            quantity=self.quantity
        )
