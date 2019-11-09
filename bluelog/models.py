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
    posts = db.relationship('Post',back_populates='category')#文章和分类

class Past(db.Model):# 文章模型
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.Datetime,default=datetime.utcnow)
    category_id = db.Column(db.Integer,db.FordignKey('category.id'))#定义外键: 传入的值是另一侧表和主键值
    category = db.relationship('Category',back_populates='posts') #定义关系属性,返回多个记录,第一个值是另一侧的模型名,它将两个表建立联系
                                                                                #定义反向引用,参数为另一侧关系属性名
    comments = db.relationship('Comment',back_populates ='post',cascade = 'all,delete-orphan') #评论的双向关系,设置了联级删除,删除文章,对应的评论也会删除

class Comment(db.Model):# 评论
    id = db.Column(db.Integer,primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean,default = False)#是否是管理员评论
    reviewed = db.Column(db.Boolean,default = False) #评论是否通过审核
    timestamp = db.Column(db.DataTime,default = datetime.utcnow,index = True)
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    post = db.relationship('Post',back_populates = 'comments')
    #邻接列表关系
    replied_id = db.Column(db.Integer,db.ForeignKey('comment.id'))
    replied = db.relationship('Comment',back_populates='replies',remote_side = [id])
    replies =db.relationship('Commit',back_populates = 'replied',cascade = 'all')







