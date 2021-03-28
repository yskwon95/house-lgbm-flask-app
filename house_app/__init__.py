import os
from flask import Flask
from flask_migrate import Migrate
from house_app.models import db
from flask import session 
from dotenv import load_dotenv

load_dotenv()
migrate = Migrate()
basedir = os.path.abspath(os.path.dirname(__file__)) 

DATABASE_URI = os.getenv("DATABASE_URI")

def create_app(config=None):
    app = Flask(__name__)
    # dbfile = os.path.join(basedir, 'houseprediction.sqlite')

    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile   
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['SECRET_KEY'] = 'thisissecret'
    
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    
    from house_app.routes import main_route,user_route,house_route
    app.register_blueprint(main_route.mainbp)
    app.register_blueprint(user_route.userbp)
    app.register_blueprint(house_route.housebp, url_prefix='/api')

    ## inserting information of contents
    # from house_app.setting.disregard_upload import init_set
    # init_set()

    return app
if __name__ == "__main__":
    print("hello")
    app = create_app()
    app.run(debug=True)

