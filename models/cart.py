from sqlalchemy  import *
from sqlalchemy.orm import backref

from extensions import db

class Cart (db.Model):
    __tablename__ = "carts"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String, default="pending")
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    user=db.relationship('User',backref=backref('carts',lazy='dynamic'))

    def total_price(self):
        total = 0
        for item in self.items:
            t=item.price*item.quantity
            total +=t