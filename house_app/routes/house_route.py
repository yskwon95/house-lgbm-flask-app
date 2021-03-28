from flask import Blueprint, render_template, request, url_for, session, redirect
from house_app.models import User,House,Apart,Bubjung,Area,db
from house_app.util.log_func import sign_in,sign_up,get_user_info,msg_processor
from house_app.util.house_func import apart_map,bubjung_map,area_map,predict_price


housebp = Blueprint('house', __name__)

# 집값 정보입력 >> 예측 >> class Houses에 입력 >>  예측 display 
@housebp.route('/predict', methods=['POST']) #action=/house/predict
def get_house():
    userid = session.get('userid', None)
    area = request.form["area"]
    bubjung = request.form["bubjung"]
    apartment = request.form["apartment"]
    size = request.form["size"]
    floor = request.form["floor"]
    year_of_built = request.form["year_of_built"]

    try:
        size = int(size)
        floor = int(floor)
        year_of_built = int(year_of_built)
    except:
        return redirect(url_for('main.house',msg_code=9))

        
    ## 1. 집정보받기
    if userid and area and bubjung and apartment and size and floor and year_of_built:
        print('start predicting')
        ## 2. db에 넣기
        get_user = User.query.filter(User.userid == session['userid']).first()
        house_up = House(area=area,bubjung=bubjung,apartment=apartment,size=size
                        ,floor=floor,year_of_built=year_of_built,user_id=get_user.id
                        ,prediction=None)
        db.session.add(house_up)
        db.session.commit()
        ## 2. 집값예측하기
        price_predicted = predict_price(house_up)

        ## 3. db에 넣기
        house_up.prediction = price_predicted
        db.session.add(house_up)
        db.session.commit()

        if price_predicted>=1000000:
            price_predicted=str(price_predicted)
            price_predicted=price_predicted[0:3]+'억'+price_predicted[3:]
            
        elif price_predicted>=100000:
            price_predicted=str(price_predicted)
            price_predicted=price_predicted[0:2]+'억'+price_predicted[2:]

        elif price_predicted>=10000:
            price_predicted=str(price_predicted)
            price_predicted=price_predicted[0]+'억'+price_predicted[1:]
        ## 4. 예측 display하기
        return redirect(url_for('main.result',prediction_price=price_predicted))
    else:
        ## 집정보를 입력해라 !
        return redirect(url_for('main.house',msg_code=6))
