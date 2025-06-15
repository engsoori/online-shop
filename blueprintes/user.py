from flask import Blueprint, render_template,request,redirect,url_for,flash
from passlib.hash import  sha256_crypt
from flask_login import login_user ,current_user ,login_required
from extensions import db
from models.user import User

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

@user.route('/user/dashboard')
@login_required
def dashboard():
    return render_template('user/dashboard.html')