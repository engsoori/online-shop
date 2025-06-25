import requests
from flask import Blueprint, render_template,request,redirect,url_for,flash
from passlib.hash import  sha256_crypt
from flask_login import login_user ,current_user ,login_required
from extensions import db
from models import cart_item
from models.cart import Cart
from models.cart_item import CartItem
from models.payment import Payment
from models.products import Product
from models.user import User
import config
user = Blueprint("user", __name__)  # تغییر نام متغیر از app به user


@user.route('/user/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')

    username = request.form.get('username')
    password = request.form.get('password')
    register = request.form.get('register')  # مقدار: 'register' یا 'login'

    if register == 'register':
        phone = request.form.get('phone')
        address = request.form.get('address')

        # بررسی پر بودن فیلدها
        if not username or not password or not phone or not address:
            flash("همه فیلدها باید پر شوند.")
            return redirect(url_for('user.login'))

        # بررسی عدم وجود کاربر تکراری
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("این نام کاربری قبلاً ثبت شده است.")
            return redirect(url_for('user.login'))

        # ثبت‌نام کاربر جدید
        new_user = User(
            username=username,
            password=sha256_crypt.encrypt(password),
            phone=phone,
            address=address
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash("با موفقیت ثبت نام شدید.")
        return redirect('/user/dashboard')

    elif register == 'login':
        user = User.query.filter_by(username=username).first()
        if user is None or not sha256_crypt.verify(password, user.password):
            flash("نام کاربری یا رمز عبور اشتباه است.")
            return redirect(url_for('user.login'))

        login_user(user)
        flash("با موفقیت وارد شدید.")
        return redirect('/user/dashboard')

    else:
        flash("درخواست نامعتبر.")
        return redirect(url_for('user.login'))


@user.route('/add_to_cart',methods=['GET'])
@login_required
def add_to_cart():
    id = request.args.get('id')
    product=Product.query.filter(Product.id==id).first_or_404()
    cart=current_user.carts.filter_by(Cart.status=='pending').first()
    if cart == None:
        cart = Cart()
        current_user.carts.append(cart)

        db.session.add(cart)


    cart=cart.cart_item.filter_by(CartItem.Product==product.id).first()
    if cart_item==None:

      item = CartItem(quantity=1)
      item.cart = cart
      item.product = product
      db.session.add(item)
    else:
        cart_item.quantity +=1
        db.session.commit()
    return redirect('/user/cart')

@user.route('/user/dashboard')
@login_required
def dashboard():
    return render_template('user/dashboard.html')



@user.route('/cart')
@login_required
def cart():
    return render_template('user/cart.html')

@user.route('/remove-from-cart',methods=['GET'])
@login_required
def remove_from_cart():
    id = request.args.get('id')
    cart_item=CartItem.query.filter(CartItem.id==id).first_or_404()
    if cart_item.quantity>1:
        cart_item.quantity-=1
    else:
       db.session.delete(cart_item)
    db.session.commit()
    return redirect('/user/cart')

@user.route('/verify',methods=['GET'])
@login_required
def verify():
    token = request.args.get('token')
    pay=Payment.query.filter(Payment.token==token).first_or_404()

    r=requests.post(config.PAYMEN_VERIFY_REQUEST_URL,
            data={
                'api':'sandbox',
                'amount':pay.price,
                'token':token
            })
    pay.status=bool(r.json()['success'])
    if pay.status:

       transaction_id=r.json()['result'][' transaction_id']
       card_pan=r.json()['result']['card_pan']
       refid=r.json()['result']['refid']


       pay.card_pan=card_pan
       pay.transaction_id=transaction_id
       pay.refid=refid
       pay.status='success'
       pay.cart.status='paid'
       flash("پرداخت موفق بود")
    else:
        flash("پرداخت با خطا مواجه شد")
        pay.status='Failed'

    db.session.commit()

    return redirect(url_for('user.dashboard'))


@user.route('/payment',methods=['GET'])
@login_required
def payment():
   cart = current_user.carts.filter_by(Cart.status == 'pending').first()
   r=requests.post(config.PAYMEN_FIRST_REQUEST_URL,
            data={
                'api':config.PAYMEN_MERCHANT,
                'amount':cart.total_price(),
                'callback':config.PAYMEN_CALLBACK,
            })
   token=r.json()['result']['token']
   url=r.json()['result']['url']

   pay=Payment(price=cart.total_price(),token=token)
   pay.cart=cart
   db.session.add(pay)
   db.session.commit()
   return redirect(url)