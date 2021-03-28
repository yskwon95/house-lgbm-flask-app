from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer(),nullable=False, primary_key=True)
    userid = db.Column(db.String(32))
    username = db.Column(db.VARCHAR(64),nullable=False)
    password = db.Column(db.VARCHAR(64),nullable=False)
    
    # houses = db.relationship("House", backref='user', lazy='subquery',cascade="all,delete")

    def __repr__(self):
        return f"User:{self.userid}/{self.username}"

class House(db.Model):
    __tablename__ = 'house'

    house_id = db.Column(db.Integer(),nullable=False, primary_key=True)
    area = db.Column(db.Text(),nullable=False)
    bubjung = db.Column(db.Text(),nullable=False)
    apartment = db.Column(db.Text(),nullable=False)
    size = db.Column(db.Text(),nullable=False)
    floor = db.Column(db.Text(),nullable=False)
    year_of_built = db.Column(db.Text(),nullable=False)
    prediction = db.Column(db.Integer(),nullable=True)
    user_id = db.Column(db.Integer(),db.ForeignKey('user.id'),nullable=False)

    def __repr__(self):
        return f"House {self.house_id}"

class Reply(db.Model):
    __tablename__ = 'reply'

    reply_id = db.Column(db.Integer,nullable=False, primary_key=True)
    userid = db.Column(db.String(32),nullable=False)
    replies = db.Column(db.Text(),nullable=False)
    time = db.Column(db.Text(),nullable=False)

    def __repr__(self):
        return f"Reply {self.userid}:{self.replies}"

class Apart(db.Model):
    __tablename__ = 'apart'

    apart_id = db.Column(db.Integer,nullable=False, primary_key=True)
    apartname = db.Column(db.Text(),nullable=False)
    apartcode = db.Column(db.Float(),nullable=False)

    def __repr__(self):
        return f"Apart:{self.apartname}{self.apartcode}"
    
class Bubjung(db.Model):
    __tablename__ = 'bubjung'

    bubjung_id = db.Column(db.Integer,nullable=False, primary_key=True)
    bubjungname = db.Column(db.Text(),nullable=False)
    bubjungcode = db.Column(db.Float(),nullable=False)

    def __repr__(self):
        return f"bubjung:{self.bubjungname}{self.bubjungcode}"
    
class Area(db.Model):
    __tablename__ = 'area'

    area_id = db.Column(db.Integer,nullable=False, primary_key=True)
    areaname = db.Column(db.Text(),nullable=False)
    areacode = db.Column(db.Float(),nullable=False)
    guK = db.Column(db.Float(),nullable=False)

    def __repr__(self):
        return f"bubjung:{self.areaname}{self.areaname}{self.guK}"

