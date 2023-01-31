from flask import Flask,request,jsonify
from flask_cors import CORS
from config import db,secret_key
from os import path,getcwd,environ
from dotenv import load_dotenv
from datetime import date

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
        @app.route("/signup", methods=['GET'])
        def signup():
            data = request.form.to_dict(flat=True)
            
            phno=data['phno']
            res=CustomerInfo.query.filter_by(phno=phno).first()
            
            if res==None:
                new_cus = CustomerInfo(
                    c_name=data['username'],
                    phno=data['phno']
                )
                db.session.add(new_cus)
                db.session.commit()
                res=CustomerInfo.query.filter_by(phno=phno).first()
                return jsonify(user_token=res.c_id)
            else:
                return jsonify(user_token=res.c_id)
#----------------------------------------------------------------------------------        
        @app.route("/placing_order",methods=["POST"])
        def placing_order():
            c_id=request.args['c_id']
            data=request.get_json()
            total_price=0
            order_ids=[]
            for order in data['orders']:
                f_name=order['f_name']
                item=FoodItems.query.filter_by(f_name=f_name).first()
                total_price+=(item.price*order['quantity'])
                
                new_order=Order(
                    f_id=item.f_id,
                    quantity=order['quantity'],
                    cost=item.price*order['quantity'],
                    date=str(date.today()),
                    c_id=c_id
                )
                db.session.add(new_order)
                db.session.commit()
                last_order=Order.query.order_by(Order.o_id.desc()).first()
                order_ids.append(last_order.o_id)

            return jsonify(order_list=order_ids,total_price=total_price)
#-------------------------------------------------------------------------------
        @app.route("/add_new_food_item",methods=["POST"])
        def add_new_food_item():
            food=request.get_json()
            new_food=FoodItems(
                price=food['price'],
                f_name=food['f_name'],
                rating=0,
                ordercount=0,
                availability=True
            )
            db.session.add(new_food)
            db.session.commit()
            return jsonify(msg="New item added successfully")
#-----------------------------------------------------------------------------------
        @app.route("/show_menu",methods=['GET'])
        def show_menu():
            avail_foods=FoodItems.query.filter_by(availability=True).all()
            items=[]
            for food in avail_foods:
                items.append({
                    'f_name':food.f_name,
                    'price':food.price,
                    'rating':food.rating,
                })
            return jsonify(available_items=items)
#-------------------------------------------------------------------------------------
        @app.route("/giving_rating",methods=["POST"])
        def giving_rating():
            data=request.get_json()
            new_rating=UserRating(
                o_id=data['o_id']
                rating=data['rating']
            )
            db.session.add(new_rating)
            f_id=Order.query.filter_by(o_id=data['o_id']).first().f_id
            fooditem=FoodItems.query.filter_by(f_id=f_id).first()
            new_ordercount=fooditem.ordercount+1
            new_rating=((fooditem.rating*fooditem.ordercount)+data['rating'])/new_ordercount
            FoodItems.query.filter_by(f_id=f_id).update({rating:new_rating})

        # db.drop_all()
        db.create_all()
        db.session.commit()

    return app


if __name__=='__main__':
    app=create_app()
    app.run(debug=True)