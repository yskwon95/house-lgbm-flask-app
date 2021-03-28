import joblib
import os
import pandas as pd
from house_app import basedir
from house_app.models import User,House,Apart,Bubjung,Area,db

def apart_map(houses):
    apartname = houses.apartment
    instan = Apart.query.filter(Apart.apartname==apartname).first()
    print(f"input:{houses.apartment}    output:{instan.apartcode}")
    return instan.apartcode

def bubjung_map(houses):
    bubjungname = houses.bubjung
    instan = Bubjung.query.filter(Bubjung.bubjungname==bubjungname).first()
    print(f"input:{houses.bubjung}    output:{instan.bubjungcode}")
    return instan.bubjungcode

def area_map(houses):
    areaname = houses.area
    instan = Area.query.filter(Area.areaname==areaname).first()
    print(f"input:{houses.area}    output:{instan.areacode} / {instan.guK}")
    return [instan.areacode,instan.guK]

def predict_price(houses): #house의 객체 넣기
    model_pkl = os.path.join(basedir, 'lgbm.pkl')
    model = joblib.load(model_pkl)
    data = {
        'area_code':area_map(houses)[0]
        , 'bubjung':bubjung_map(houses)
        , 'apartment':apart_map(houses)
        , 'size':float(houses.size)
        , 'floor':int(houses.floor)
        , 'year_of_built':int(houses.year_of_built)
        , 'year_sale':2021.0
        , 'month_sale':35.0
        , 'family':185109.0
        , 'popul':400989.0
        , 'car_reg':114020.0
        , 'popul_moving':133111.0
        , 'foreign_stock':787.9
        , 'country_10':1.73
        , 'company_3':2.14
        , 'CD91':0.68
        , 'sobija_mulga':0.5
        , 'argri':9.7
        , 'factory':-0.9
        , 'public_serv':-2.0
        , 'origin_mulga':0.9
        , 'born':3483.0
        , 'death':3823.0
        , 'marry':3802.0
        , 'divorce':1498.0
        , 'DJI':30820.998000000003
        , 'IXIC':13177.2015
        , 'VIX':24.8815
        , 'SSEC':3566.428000000001
        , 'DE30':13823.259
        , 'FCHI':5589.485000000001
        , 'NG':2.65315
        , 'GC':43.17700000000001
        , 'CL':80.945
        , 'guK':area_map(houses)[1]
        , 'KRX':4064.5805
    }
    data_f = pd.DataFrame([data])

    prediction = model.predict(data_f) # 판다스형태로 데이터넣기

    return int(prediction[0])
