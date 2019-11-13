from flask import Flask,redirect,url_for,render_template
from flask_mail import Mail

app = Flask(__name__)


#敏感信息,在env中获取
app.config.update(
    MAIL_SERVER = os.getenv('MAIL_SERVER'),
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USERNAME = os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=('Wang ...',os.getenv('MAIL_USERNAME'))
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
def send_mail(subject,to,body):
    message = Message(subject,recipients=[to],body = body)
    mail.send(message)

@app.route('/subscribe',methods=['GET','POST'])
def subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data
        send_mail('订阅成功',email,'你好,欢迎订阅...')
        flash('提交成功')
        return redirect(url_for('index'))
    return render_template('index.html',form = form )
