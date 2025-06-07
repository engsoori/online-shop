from flask import Flask, Blueprint

# تعریف Blueprint
general = Blueprint("general", __name__)

@general.route('/')
def home():
    return 'this is main page'

@general.route('/about')
def about():
    return 'about us'
