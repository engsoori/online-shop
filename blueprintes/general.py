from flask import Flask, Blueprint ,render_template

from blueprintes.admin import products
from models.products import Product

# تعریف Blueprint
general = Blueprint("general", __name__)

@general.route('/')
def main():
    products=Product.query.all()
    return render_template('main.html',products=products)

@general.route('/about')
def about():
    return render_template('about.html')
