from flask import Blueprint, render_template, request, session, redirect, url_for
from flask import abort
from models.products import Product
import config
from extensions import db
import  models.user
app = Blueprint("admin", __name__)

@app.before_request
def before_request():
    if session.get('admin_login',None)==None and request.endpoint != 'admin.login':
        abort(403)

@app.route('/admin/login' , methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
       username = request.form.get('username',None)
       password = request.form.get('password',None)

       if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
           session['admin_login'] = username
           return  redirect(url_for("admin.dashboard"))
       else:
           return redirect(url_for("admin.dashboard"))
   else:
    return render_template('admin/login.html')
@app.route('/product/<int:id>/<name>')
def product(id,name):
    product = Product.query.filter_by(id=id, name=name).first_or_404()

    return render_template('admin/product.html', product=product)
@app.route('/admin/dashboard')
def dashboard():
           return render_template("admin/dashboard.html")


@app.route('/admin/dashboard/products', methods=['GET', 'POST'])
def products():
    if request.method == "GET":
        products = Product.query.all()
        return render_template("admin/products.html" , products=products)
    else:
        name = request.form.get('name',None)
        description = request.form.get('description',None)
        price = request.form.get('price',None)
        active = request.form.get('active',None)
        file = request.files.get('cover',None)
        p=Product(name=name,description=description,price=price)
        if active== None:
           p.active = 0
        else:
           p.active = 1

        db.session.add(p)
        db.session.commit()

        file.save(f'static/cover/{p.id}.jpg')
        return "done"

@app.route('/admin/dashboard/edit-product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.filter_by(id=id).first_or_404()

    if request.method == "POST":
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = request.form.get('price')
        file = request.files.get('cover', None)
        product.active = 1 if request.form.get('active') else 0

        db.session.commit()
        if file != None:
            file.save(f'static/cover/{product.id}.jpg')
        return redirect(url_for('admin.products'))  # یا هر صفحه‌ای که لیست محصولات رو نشون میده

    return render_template("admin/edit-product.html", product=product)
