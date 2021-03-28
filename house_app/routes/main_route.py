from flask import Blueprint, render_template, request, url_for, session, redirect
from house_app.models import User,House,Apart,Bubjung,Area,db, Reply
from house_app.util.log_func import sign_in,sign_up,get_user_info,msg_processor
import datetime

mainbp = Blueprint('main', __name__)




@mainbp.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == "GET": # 인덱스페이지로 왔을 때
        if 'userid' in session: # 로그인 되어 있으면
            return redirect(url_for('main.home')) # 홈페이지로 리다이렉트
        else: # 로그인 안되어있면
            msg_code = request.args.get('msg_code', None)
            alert_msg = msg_processor(msg_code) if msg_code is not None else None
            return render_template('index.html', alert_msg=alert_msg) # 페이지 렌더링(로그인페이지)

    elif request.method == "POST": # 로그인 폼 제출할경우
        input_value = request.form # 폼 받고
        if sign_in(input_value): # sigin하는 함수 돌려서, 로그인 성공하면
            session['userid'] = input_value['userid'] # userid는 세션의 아이디가 된다
            return redirect(url_for('main.home'))# 홈페이지로 리다이렉트
        else:
            return redirect(url_for('main.index', msg_code=1))


@mainbp.route('/home',methods=['GET','POST'])
def home():
    if request.method == 'GET':
        if 'userid' in session:
            msg_code = request.args.get('msg_code', None)
            alert_msg = msg_processor(msg_code) if msg_code is not None else None
            repl = Reply.query.all()
            return render_template('home.html', userid=session['userid'], alert_msg=alert_msg, repl=repl)

        else:
            return redirect(url_for('main.index',msg_code=0))
    else:
        userid = session.get('userid', None)
        reply = request.form["reply"]
        if reply :
            now = datetime.datetime.now()
            time = f"{now.year:4d}-{now.month:02d}-{now.day:02d} {now.hour:02d}:{now.minute:02d}:{now.second:02d}"
            repl_up = Reply(userid=userid, replies=reply, time=time)
            db.session.add(repl_up)
            db.session.commit()
            return redirect(url_for('main.index',msg_code=6))
        else:
            return redirect(url_for('main.index',msg_code=8))


@mainbp.route('/houses')
def house():
    if 'userid' in session:
        finding = request.args.get('finding', None)
        msg_code = request.args.get('msg_code', None)
        alert_msg = msg_processor(msg_code) if msg_code is not None else None

        from house_app.setting.apart_list import apt_lst
        bubjung_list = Bubjung.query.all()
        area_list = Area.query.all()
        apart_list = Apart.query.filter(Apart.apartname.like(f"%{finding}%")).all()
        print('-'*100)
        print(apart_list)



        return render_template('houses.html', userid=session['userid']
                                            , alert_msg=alert_msg
                                            , apart_list=apart_list
                                            , bubjung_list=bubjung_list
                                            , area_list=area_list)
    else:
        return redirect(url_for('main.index',msg_code=0))



@mainbp.route('/result')
def result():
    if 'userid' in session:
        msg_code = request.args.get('msg_code', None)
        alert_msg = msg_processor(msg_code) if msg_code is not None else None
        prediction_price = request.args.get('prediction_price', None)
        return render_template('result.html', userid=session['userid']
                                            , alert_msg=alert_msg
                                            , prediction_price=prediction_price)
                                            
    else:
        return redirect(url_for('main.index',msg_code=0))

@mainbp.route('/map')
def map():
    if 'userid' in session:
        msg_code = request.args.get('msg_code', None)
        alert_msg = msg_processor(msg_code) if msg_code is not None else None
        return render_template('map.html', userid=session['userid'], alert_msg=alert_msg)
    else:
        return redirect(url_for('main.index',msg_code=0))
        

@mainbp.route('/history')
def history():
    if 'userid' in session:
        msg_code = request.args.get('msg_code', None)
        alert_msg = msg_processor(msg_code) if msg_code is not None else None

        get_user = User.query.filter(User.userid == session['userid']).first()
        house_list = House.query.filter(House.user_id==get_user.id).all()
    
        return render_template('history.html', userid=session['userid']
                                             , alert_msg=alert_msg
                                             , house_list=house_list)
    else:
        return redirect(url_for('main.index',msg_code=0))



@mainbp.route('/finding',methods=['GET','POST'])
def finding():
    if request.method == 'GET':
        if 'userid' in session:
            ## 아파트검색창
            msg_code = request.args.get('msg_code', None)
            alert_msg = msg_processor(msg_code) if msg_code is not None else None
            return render_template('search.html', userid=session['userid']
                                                , alert_msg=alert_msg)
        else:
            return redirect(url_for('main.index',msg_code=0))

    elif request.method == 'POST':
        ## 검색한 결과를 redirect해서 houses로 반환
        finding = request.form["finding"]
        print(finding)
        if finding:
            apart_list = Apart.query.filter(Apart.apartname.like(f"%{finding}%")).first()
            print(apart_list)
            if apart_list:
                return redirect(url_for('main.house',finding=finding))
            else :
                return redirect(url_for('main.finding',msg_code=7))

        else:
            return redirect(url_for('main.finding',msg_code=6))
