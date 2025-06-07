from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask import Blueprint, render_template, request, redirect, url_for, session
from blueprintes.admin import app as admin
from blueprintes.general import  general
import config
import extensions

from models.products import Product
from models.user import User


app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(admin)
app.secret_key = 'your_secret_key'


app.config['SQLALCHEMY_DATABASE_URI']=config.SQLALCHEMY_DATABASE_URI
extensions.db.init_app(app)

Csrf=CSRFProtect(app)

with app.app_context():
    extensions.db.create_all()



if __name__ == '__main__':
    app.run(debug=True)
