from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
import init_tables

Base = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=False)

    #TODO
    
    app.config.from_object('config.config.Config')
    
    Base.init_app(app)
    
    with app.app_context():
        
        # import routes
        from routes.route_person import api_persona
        
        # add routes
        app.register_blueprint(api_persona)

        # import all models
        init_tables.init()
        
        # create all tables
        Base.create_all()
    
    return app