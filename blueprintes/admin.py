from flask import Blueprint
import  models.user
app = Blueprint("admin", __name__)



@app.route('/admin')
def admin():
    return 'this is admin'