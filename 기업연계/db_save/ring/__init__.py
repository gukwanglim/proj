from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    # ORM
    db.init_app(app)             # init_app 메서드를 이용해 app에 등록
    migrate.init_app(app, db)   
    from . import models         # 플라스크의 migrate 기능을 인식하기 위해 models를 import

    # 블루프린트
    from .views import main_views, index_views, auth_views, shop_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(index_views.bp)
    app.register_blueprint(auth_views.bp)
    app.register_blueprint(shop_views.bp)


    return app 
