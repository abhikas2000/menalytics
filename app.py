from flask import Flask,request,jsonify
from flask_cors import CORS
from config import db,secret_key
from os import path,getcwd,environ
from dotenv import load_dotenv

from models.customer_info import CustomerInfo
from models.food_items import FoodItems
from models.order import Order
from models.user_rating import UserRating

load_dotenv(path.join(getcwd(),'.env'))

def create_app():
    app=Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']=environ.get('DB_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
    app.config['SQLALCHEMY_ECHO']=False
    app.secret_key=secret_key

    db.init_app(app)
    print("DB Initialized Successfully")

    CORS(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()

        #create routs here

    return app


if __name__=='__main__':
    app=create_app()
    app.run(debug=True)