from sqlalchemy  import *
from extensions import db
from flask_login import UserMixin
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False, index=True)
    password = db.Column(db.String, nullable=False, index=True)
    phone = db.Column(db.String(11), nullable=False, index=True)
    address = db.Column(db.String, nullable=False, index=True)