from flask import Flask, Blueprint ,render_template

from blueprintes.admin import products
from models.products import Product

# تعریف Blueprint
general = Blueprint("general", __name__)

@general.route('/')
def main():
    products=Product.query.filter(Product.active==1).all()
    return render_template('main.html',products=products)
@general.route('/product/<int:id>/<name>')
def product(id,name):
    product=Product.query.filter(Product.id==id).filter(Product.name==name).filter(Product.active==1).first_or_404()
    return render_template('product.html',product=product)

@general.route('/about')
def about():
    return render_template('about.html')
