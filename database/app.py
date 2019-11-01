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
        db.session.commit()
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
    form = DeleteNoteForm()
    return render_template('index.html',notes=notes,form = form)

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

#delate
#删除表单
class DeleteNoteForm(FlaskForm):
    submit = SubmitField('Delete')

@app.route('/delete/<int:note_id>',methods=['POST'])
def delete_note(note_id):
    form = DeleteNoteForm()
    if form.validate_on_submit():
        note = Note.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        flash('笔记已经删除')
    else:
        abort(400)
    return redirect(url_for('index'))
    
#配置flask shell上下文

@app.shell_context_processor
def make_shell_context():
    return dict(db=db,Note = Note,Author=Author,Article=Article,
    Writer=Writer,Book=Book) #等同于{'db':db,'Note':Note}
# (my_flask) wang@wang:~/my_web$ flask shell
# Python 3.6.8 (default, Oct  7 2019, 12:59:55) 
# [GCC 8.3.0] on linux
# App: app [development]
# Instance: /home/wang/my_web/database/instance
# >>> db
# <SQLAlchemy engine=sqlite://///home/wang/my_web/database/data.db>
# >>> Note
# <class 'app.Note'>
# >>> 

#一对多:
#第一步:定义外键,在"多"的一侧
#第二步:定义关系属性,在"一"的一侧
#第三步:建立关系
class Author(db.Model):     #作者
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(70),unique=True)
    phone = db.Column(db.String(20))
    articles = db.relationship('Article')#使用relationship()关系函数定义关系属性,这个关系属性返回多个记录(集合关系属性).
    #第一个参数为关系另一侧的模型名称,它将两个表建立关系,
    #被调用时,Sqlalchemy找到关系的另一侧的外键字段,然后反向查询article表中author_id值为当前表主键值的记录,返回包含这些记录的列表
class Article(db.Model):    #文章
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50),index=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer,db.ForeignKey('author.id'))#定义外键,传入的值是另一侧的表名和主键字段名


# >>> foo=Author(name="Foo")
# >>> spam=Article(title="Spam")
# >>> ham = Article(title="Ham")

# >>> db.session.add(foo)
# >>> db.session.add(spam)
# >>> db.session.add(ham)
# >>> foo.articles.append(spam)#建立关系,或者spam.author_id = 1
# >>> foo.articles.append(ham)

# >>> db.session.commit()#提交到数据库

#一对多的双向关系
#1. 定义外键,在"多"的一侧
#2. 定义关系属性,在两侧,并且使用back_populates定义反向引用来连接另一侧,参数值为另一侧的关系属性名
#3. 建立关系
class Writer(db.Model):#作者
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(70),unique = True)
    books = db.relationship('Book',back_populates='writer')

class Book(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),index=True)
    writer_id = db.Column(db.Integer,db.ForeignKey('writer.id'))
    writer = db.relationship('Writer',back_populates='books')

# >>> king = Writer(name='Stephen King')
# >>> carrie = Book(name='Carrit')
# >>> it = Book(name='IT')
# >>> db.session.add(king)
# >>> db.session.add(carrie)
# >>> db.session.add(it)
# >>> db.session.commit()

# >>> carrie.writer = king #建立关系
# >>> carrie.writer
# <Writer 1>
# >>> it.writer = king  #建立关系
# >>> king.books
# [<Book 1>, <Book 2>]



#多对多

#关联表
#使用db.Table()定义关联表,第一个参数是关联表名,
association_table = db.Table('association',
                            db.Column('student_id',db.Integer,db.ForeignKey('student.id')),
                            db.Column('teacher_id',db.Integer,db.ForeignKey('teacher.id'))
                            )

class Student(db.Model):#学生表
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(70),unique=True)
    grade = db.Column(db.String(20))
    teachers = db.relationship('Teacher',
                        secondary=association_table,
                        back_populates='students')


class Teacher(db.Model):#教师表
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.string(70),unique=True)
    office = db.Column(db.String(20))
    students = db.relationship('Student',
                            secondary=association_table,
                            back_populates='teachers')





#使用flask-migrate迁移数据库
#虚拟环境下,pip3 install flask-migrate





