import os
from flask import Flask,redirect,url_for,render_template,flash
from flask_mail import Mail,Message

app = Flask(__name__)


#敏感信息,在env中获取
app.config.update(
    SECRET_KEY = os.getenv('SECRET_KEY','secret string'),
    MAIL_SERVER = os.getenv('MAIL_SERVER'), #发信服务器
    MAIL_PORT = 587,    #发信端口
    MAIL_USE_TLS = True,    #TLS加密
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'), #服务器用户名
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'), #密码  qq邮箱为授权码
    MAIL_DEFAULT_SENDER=('Wang ...',os.getenv('MAIL_USERNAME'))# 发信人  使用SMTP服务时,发信人和用户名必须一样
)

mail = Mail(app)

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,Email
#发信表单
class SubscribeForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Subscribe')

#通用发信函数
#subject主题   recipients为收件人邮件地址的列表  body为正文
def send_mail(subject,to,body):
    message = Message(subject,recipients=[to],body = body) #邮件通过Message类构建
    message.body = '纯文本正文'     #message.body   纯文本正文
    message.html = '<p style="color:red">我是html正文</p>'#html的邮件,
      #如果用户邮件系统不支持html,则显示纯文本正文,所以应该编写两种格式的邮件
    #或者使用模板发送邮件
    #message.html = render_template('邮件.html')
    mail.send(message)          #调用maile.send()发送邮件

@app.route('/',methods=['GET','POST'])
def index():
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data
        send_mail('订阅成功',email,'巧巧吃屁') #调用通用发信函数
        flash('提交成功')
        return redirect(url_for('index'))
    return render_template('index.html',form = form )




