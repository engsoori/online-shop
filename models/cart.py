from sqlalchemy  import *
from extensions import db

class Cart (db.Model):
    __tablename__ = "carts"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.string, default="pending")
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    user=db.relationship('User',backref='carts')
