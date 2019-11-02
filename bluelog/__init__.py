import os
from flask import Flask,render_template,request
from bluelog.settings import config
from bluelog.extensions import bootstrap,db,moment,ckeditor,mail
from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp

def create_app(config_name = None):
    if  config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')#优先在.env和flaskenv加载配置
    
    app = Flask('bluelog')

    app.config.from_object(config[config_name])

    register_logging(app)#注册日志处理
    register_extensions(app) #注册扩展(扩展初始化)
    register_blueprints(app)  #注册蓝本
    register_commands(app) #注册自定义命令
    register_errors(app) #注册错误处理函数
    register_shell_context(app) #注册shell上下文处理函数
    register_template_context(app) #注册模板上下文处理函数
    return app

def register_logging(app):
    pass

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    mail.init_app(app)

def register_blueprints(app):
    app.register_blueprint(blog_bp) #注册蓝本
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(auth_bp,url_prefix='/auth')

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db)


def register_template_context(app):
    pass

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500


def register_commands(app):
    pass