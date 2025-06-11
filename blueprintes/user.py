from flask import Blueprint, render_template,request,redirect,url_for
from passlib.hash import  sha256_crypt
from flask_login import login_user
from extensions import db
from models.user import User

user = Blueprint("user", __name__)  # تغییر نام متغیر از app به user

@user.route('/user/login',methods=['GET','POST'])
def login():  # نام تابع رو از user به login تغییر دادیم
    if request.method == 'GET':
       return render_template('user/login.html')
    else:
        register = request.form.get('register',None)
        username = request.form.get('username',None)
        password = request.form.get('password',None)
        phone = request.form.get('phone',None)
        address = request.form.get('address',None)

    if register != None:
        user=User(username=username,password=sha256_crypt.encrypt(password),phone=phone,address=address)
        db.session.add(user)
        db.session.commit()

        return redirect('/user/dashboard')

    return 'done'