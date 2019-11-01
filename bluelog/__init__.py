import os
from flask import Flask
from bluelog.settings import config
from bluelog.extensions import bootstrap,db,moment,ckeditor,mail

def create_app(config_name = None):
    if  config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')#优先在.env和flaskenv加载配置
    
    app = Flask('bluelog')
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)
    
    app.config.from_object(config[config_name])

    app.register_blueprint(blog_bp) #注册蓝本
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(auth_bp,url_prefix='/auth')
    return app