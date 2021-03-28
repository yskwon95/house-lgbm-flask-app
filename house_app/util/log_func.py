from house_app.models import User,db

def sign_in(input_value):
    print('-'*100)

    input_id = input_value['userid']
    input_password = input_value['password']
    print(f'sign_in ID : {input_id}   PW : {input_password}')

    if User.query.filter(User.userid==input_id).first(): 
        if input_password == User.query.filter(User.userid==input_id).first().password:
            print('login success')
            return True
        else:
            print('password unmatched')
            return False
    else:
        print('id unidentified')
        return False


def sign_up(input_value):
    user = User.query.filter(User.userid==input_value['userid']).first()
    print('-'*100)
    print('sign_up USER :',user)
    if user:
        print('id already exists')
        return False
    else:
        user_data = User(
            userid=input_value['userid'],
            password=input_value['password'],
            username=input_value['username'])
        db.session.add(user_data)
        db.session.commit()
        return True

def get_user_info(now_user):
    user_info = User.query.filter(User.userid==now_user).first()

    return user_info.username, user_info.userid

def msg_processor(msg_code):

    msg_code = int(msg_code)

    msg_list = [
        ('로그인이 필요합니다.','warning'),
        ('로그인에 실패하였습니다. 아이디와 비밀번호를 확인해주세요','warning'),
        ('로그아웃 되었습니다.','success'),
        ('ID가 성공적으로 만들어졌습니다.','success'),
        ('회원가입이 완료되었습니다.','success'), #4
        ('존재하는 아이디 입니다.','warning'), #5
        ('채워지지 않은 빈칸이 있습니다.','warning'), #6
        ('검색된 아파트가 없습니다.','warning'), #7
        ('댓글이 작성되었습니다.','success'),#8
        ('단위면적,층,건축년도는 숫자로 입력해주세요.','warning')#9

    ]

    print('msg_code : ',msg_list[msg_code][0])
    return {
        'msg':msg_list[msg_code][0],
        'type':msg_list[msg_code][1]
    }
