# -*- coding: utf-8 -*-
import os
from flask import Flask,render_template,request
from bluelog.settings import config
from bluelog.extensions import bootstrap,db,moment,ckeditor,mail
from bluelog.blueprints.admin import admin_bp
from bluelog.blueprints.auth import auth_bp
from bluelog.blueprints.blog import blog_bp
from bluelog.models import Admin,Category,Post,Comment#flask shell上下文处理函数需要调用

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

def register_shell_context(app):#shell上下文处理函数
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db,Admin=Admin,Post=Post,Comment=Comment,Category=Category)


def register_template_context(app):#模板上下文处理
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        return dict(admin = admin,categories = categories)

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

import click
def register_commands(app):
    #生成博客虚拟数据
    @app.cli.command()
    @click.option('--category',default = 10,help = '类别的数量,默认是10.')
    @click.option('--post',default = 50,help = '帖子的数量,默认是50.')
    @click.option('--comment',default = 500,help='回复的数量,默认是500.')
    def forge(category, post,comment):
        """生成类别,帖子,回复的虚拟数据"""
        from bluelog.fakes import fake_admin, fake_categories, fake_posts, fake_comments
        db.drop_all()
        db.create_all()

        click.echo('生成管理员...')
        fake_admin()

        click.echo('生成 %d  类别 ' %category)
        fake_categories(category)

        click.echo('Generating %d posts...' %post)
        fake_posts(post)

        click.echo('generating %d comments...' %comment)
        fake_comments(comment)

        click.echo('Done.')
    #为了正常生成数据,顺序必须是管理员--->分类--->文章--->评论
    #使用flask forge生成虚拟数据
    #使用 flask forge --categort=20 --post=200 --comment=1000           生成自定义数量的虚拟数据


















