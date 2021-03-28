from house_app.models import User,House,Apart,Bubjung,Area,db
import pandas as pd

def init_set():
    apart = r"C:\Users\aodl3\Desktop\AI Bootcamp\project33\house_app\setting\apart.csv"
    area = r"C:\Users\aodl3\Desktop\AI Bootcamp\project33\house_app\setting\area.csv"
    bubjung = r"C:\Users\aodl3\Desktop\AI Bootcamp\project33\house_app\setting\bubjung.csv"


    apt = pd.read_csv(apart)
    apt.columns = ['apart_id','apartname','apartcode']
    aptlist = apt.to_dict('list')
    
    ara = pd.read_csv(area)
    ara.columns = ['area_id','areaname','areacode','guK']
    aralist = ara.to_dict('list')

    bub = pd.read_csv(bubjung)
    bub.columns = ['bubjung_id','bubjungname','bubjungcode']
    bublist = bub.to_dict('list')

    print('inserting apartment')
    for row in zip(aptlist['apart_id'],aptlist['apartname'],aptlist['apartcode']):
        apart_id = int(row[0])
        apartname = str(row[1])
        apartcode = float(row[2])
        apart_up = Apart(apart_id=apart_id
                        ,apartname=apartname
                        ,apartcode=apartcode)
        db.session.add(apart_up)
        db.session.commit()
    print('apartment complete')

    for row in zip(aralist['area_id'],aralist['areaname'],aralist['areacode'],aralist['guK']):
        area_id = int(row[0])
        areaname = str(row[1])
        areacode = float(row[2])
        guK = float(row[3])
        area_up = Area(area_id=area_id
                      ,areaname=areaname
                      ,areacode=areacode
                      ,guK=guK)
        db.session.add(area_up)
        db.session.commit()
    print('area complete')

    for row in zip(bublist['bubjung_id'],bublist['bubjungname'],bublist['bubjungcode']):
        bubjung_id = int(row[0])
        bubjungname = str(row[1])
        bubjungcode = float(row[2])
        bub_up = Bubjung(bubjung_id=bubjung_id
                        ,bubjungname=bubjungname
                        ,bubjungcode=bubjungcode)
        db.session.add(bub_up)
        db.session.commit()
    print('bubjung complete')

    return