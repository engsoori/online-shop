from flask import Flask

from blueprintes.general import app as general
import config
import extensions
app = Flask(__name__)
app.register_blueprint(general)




app.config['SQLALCHEMY_DATABASE_URI']=config.SQLALCHEMY_DATABASE_URI
extensions.db.init_app(app)


with app.app_context():
    extensions.db.create_all()


if __name__ == '__main__':
    app.run()

