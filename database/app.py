from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
db = SQLAlchemy(app)  #初始化

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL','sqlite:////'+os.path.join(app.root_path,'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False#是否追踪对象的修改


class   Note(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    body = db.Column(db.Text)


import click
@app.cli.command()#使用自定义命令创建库和表
def initdb():
    db.create_all()
    click.echo('表已创建')

@app.cli.command()#自定义命令删除表
def dropdb():
    db.drop_all()
    click.echo('表已删除')

