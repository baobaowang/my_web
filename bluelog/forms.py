

#登录表单
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired
class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(1,20) ] )   #用户名
    password = PasswordField('Password',validators=[DataRequired(),lenght(8,128) ] ) #密码
    remember = BooleanField('Remember me') #记住我
    submint = SubmitField('Log in') #提交

#文章表单
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,SelectField
from wtforms.validators import DataRequired,Length
from bluelog.models import Category
class PostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired(),Length(1,60)] ) #标题
    category = SelectField("Category",coerct = int,default=1 ) #下拉列表   分类选择
    body = CKEditorField('Body',validators=[DataRequired()] )   #正文
    submint = SubmitField()  #提交

    def __init__(self, *args,**kwargs):# 构造函数
        super(PostForm,self).__init__(*args,**kwargs)
        self.category.choices = [(category.id,category.name)                                                                                                #这是几个意思?
        for category in Category.query.order_by(Category.name).all() ]



#分类表单
from wtforms import StringField, SubmitField,ValidationError
from wtforms.validators import DataRequired 
from bluelog.models import Category
class CategoryForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(),Length(1,30)])
    submit= SubmitField()
    def validate_name(self,field): #自定义行内验证器                分类的名称不能重复
        if Category.quey.filter_by(name=field.date).first():
            raise ValidationError('Name already in user. ')
 
# 评论表单
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Email,URL,Length,Optional
class CommentForm(FlaskForm):
    author = StringField('Name',validators=[DataRequired(),Length(1,30)])
    email = StringField('Email',validators=[DataRequired(),Email(),Length(1,254)])
    site = StringField('Site',validators=[Optional(),URL(),Length(0,255)])      #Optional()验证器:字段可为空
    body= TextAreaField('Comment',validators=[DataRequired()])
    submit = SubmitField()

#管理员评论表单
from wtforms import HiddenField
class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()























