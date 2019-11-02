# -*- coding: utf-8 -*-

from bluelog.extensions import db
from datetime import datetime


class Admin(db.Model): #管理员模型
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

class Category(db.Model): #分类
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(30),unique = True)

class Past(db.Model):# 文章模型
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.Datetime,default=datetime.utcnow

class 