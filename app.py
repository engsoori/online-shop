from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask import Blueprint, render_template, request, redirect, url_for, session,flash
from blueprintes.admin import app as admin
from blueprintes.general import  general
from blueprintes.user import user
import config
import extensions
from models.products import Product
from models.user import User
from flask_login import LoginManager, current_user

app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(admin)
app.secret_key = 'your_secret_key'
app.register_blueprint(user)

app.config['SQLALCHEMY_DATABASE_URI']=config.SQLALCHEMY_DATABASE_URI
extensions.db.init_app(app)

Csrf=CSRFProtect(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    flash('وارد حساب کاربریتان شوید')
    return redirect(url_for('user.login'))


with app.app_context():
    extensions.db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

