from  flask_sqlalchemy import SQLAlchemy
import time
from models.products import Product

db = SQLAlchemy()

def get_current_time():
    return round(time.time())