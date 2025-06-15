from sqlalchemy  import *
from extensions import db

class Payment (db.Model):
    __tablename__ = "payments"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.string, default="pending")
    cart_id= db.Column(db.Integer, db.ForeignKey('carts.id'),nullable=False)
    cart=db.relationship('Cart',backref='payments')
    