from flask import Blueprint, render_template, request, url_for, session, redirect
from house_app.models import User,House,Apart,Bubjung,Area,db
from house_app.util.log_func import sign_in,sign_up,get_user_info,msg_processor

userbp = Blueprint('user', __name__)


# 로그아웃
@userbp.route('/logout')
def logout_func():
    if 'userid' in session:
        session.pop('userid', None) # 세션에서 아이디 뺌으로써 로그아웃
    return redirect(url_for('main.index',msg_code=2)) # 로그아웃되었습니다 보여주기

# 회원가입
@userbp.route('/register', methods=['GET', 'POST'])
def sign_up_page():
    if request.method == "GET":
        if 'userid' in session: #로그인되어있으면
            return redirect(url_for('main.index')) # 홈페이지로 리다이렉트
        else: # 안되어있으면
            msg_code = request.args.get('msg_code', None)
            alert_msg = msg_processor(msg_code) if msg_code is not None else None
            return render_template('sign_up.html', alert_msg=alert_msg) # sign up 페이지 렌더링

    elif request.method == "POST": # 만약 signup 포스트 요청 들어오면
        input_value = request.form # 폼받고
        if input_value['userid'] and input_value['password'] and input_value['username'] : # 폼이 다 채워져있으면
            if sign_up(input_value): # 사인업시키고
                return redirect(url_for('main.index',msg_code=4)) # 로그인창으로 리다이렉트
            else: # 아이디가 존재하면
                return redirect(url_for('user.sign_up_page',msg_code=5))
        else: # 폼이안채워져있으면
            return redirect(url_for('user.sign_up_page',msg_code=6))
    
