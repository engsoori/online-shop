import os

from models.payment import Payment

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "database.db")
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="1234"
SECRET_KEY="secret"
PAYMEN_MERCHANT="sandbox"
PAYMEN_CALLBACK="https://localhost:5000/verify"
PAYMEN_FIRST_REQUEST_URL='https://sandbox.shepa.com/api/v1/token'
PAYMEN_VERIFY_REQUEST_URL='https://sandbox.shepa.com/api/v1/verify'