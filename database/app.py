from flask import Flask,url_for,render_template,redirect,flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret string')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL','sqlite:////'+os.path.join(app.root_path,'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False#是否追踪对象的修改
db = SQLAlchemy(app)  #初始化
#新建数据库表
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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

#在视图函数操作数据库

#先创建个新笔记的表单
from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from wtforms.validators import DataRequired
class NewNoteForm(FlaskForm):
    body = TextAreaField('Body',validators=[DataRequired()])
    submit = SubmitField('Save')

#渲染新笔记模板
@app.route('/new',methods=['GET','POST'])
def new_note():
    form = NewNoteForm()
    if form.validate_on_submit():
        body = form.body.data
        note = Note(body=body)
        db.session.add(note)
        db.session.commti()
        flash('这条笔记已经保存')
        return  redirect(url_for('index'))
    return render_template('new_note.html',form=form)

# @app.route('/')
# def index():
#     return render_template('index.html')

#Read
@app.route('/')
def index():
    notes = Note.query.all()
    return render_template('index.html',notes=notes)

#Update
#更新表单
class EditNoteForm(FlaskForm):
    body = TextAreaField('Body',validators=[DataRequired()])
    submit = SubmitField('Update')

@app.route('/edit/<int:note_id>',methods=['GET','POST'])
def edit_note(note_id):
    form = EditNoteForm()
    note = Note.query.get(note_id)
    if form.validate_on_submit():
        note.body = form.body.data
        db.session.commit()
        flash('笔记已更新')
        return redirect(url_for('index'))
    form.body.data = note.body
    return render_template('edit_note.html',form = form )



