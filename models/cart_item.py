from sqlalchemy  import *
from extensions import db

class CartItem (db.Model):
    __tablename__ = "cart_items"
    id = db.Column(db.Integer, primary_key=True)
    product_id= db.Column(db.Integer, db.ForeignKey('products.id'),nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'), nullable=False)
    quantity= db.Column(db.Integer)
    price = db.Column(db.Integer)
    product = db.relationship('Product', backref='cart_items')
    cart = db.relationship('Cart', backref='cart_items',lazy='dynamic')