from flask import Flask,request,redirect,url_for
app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"

#访问/hello?name = wangnan时会显示 hello wangnnan
@app.route('/hello')
def hello():
    name = request.args.get('name','Flask')#request获取请求报文中的数据
    return "hello  %s" %name



#设置监听的http方法
@app.route('/get_post',methods=['GET','POST'])
def get_post():
    return '同时监听GET和POST请求'

#url处理
@app.route('/goback/<int:year>')
def goback(year):
    return "今年你%s岁了" %(2019-year)

#使用location重定向到其他网址
@app.route('/my_location')
def my_location():
    return '重定向',302,{'Location':'http://www.baidu.com'}

#使用redirect重定向到其他网址
@app.route('/my_redirect')
def my_redirect():
    return redirect('http://www.baidu.com')

#使用url_for重定向到其他视图
@app.route('/my_urlfor')
def my_urlfor():
    return redirect(url_for('hello'))

#返回错误响应
from flask import abort
@app.route('/404')
def not_found():
    abort(404)#abort前不需要使用return,但一旦使用abort,之后的代码将不会执行


#响应格式
from flask import make_response
@app.route('/my_plain')
def  my_plain():
    response = make_response('hello,world')
    response.mimetype = 'text/plain'
    return response

#使用json模块返回JSON响应
from flask import json
@app.route('/my_json')
def my_json():
    date = {
        'name':'wangnan',
        'gender':'male',
    }
    #使用dumps()将字典序列化为json字符串
    response = make_response(json.dumps(date))
    response.mimetype='application/json'
    return response


#更多的是使用jsonify()自动序列化并返回JSON响应
from flask import jsonify
@app.route('/my_jsonify')
def my_jsonify():
    date = {
        'name':'wangnan',
        'gender':'male',
    }
    return jsonify(date)
    #或者
    #return jsonify(name='wangnan',gender='male')
    #或者
    #return jsonify({'name':'wangnan','gender':'male'})
    #自定义响应类型
    #return jsonify(message='Error!'),500


#生成重定向响应设置Cookie
from flask import Flask,make_response
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name',name)
    return response

#Session
#设置秘钥
app.secret_key='secret string'
#或者写入.env中:
# SECRET_KEY=secret string
#然后在程序中使用os模块的getenv()调用
#app.secret_key=os.getenv('SECRET_KEY','secret string')
#getenv()第二个参数作用是如果没有获取到对应的环境变量则使用第二个参数

#使用Session模拟用户认证
from flask import redirect,url_for,session
@app.route('/my_session')
def login():
    session['logged_in'] =True #写入Session,Session对象可以像字典一样操作
    return redirect(url_for('redirect_session'))#重定向到redirect_session视图


#根据用户认证状态返回不同的内容
from flask import request,session
@app.route('/redirect_session')
def redirect_session():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name','备用值')#这行没什么卵用
        response = "hello %s" %name
    if 'logged_in' in session:
        response +='[Authenticated]'
    else:
        response += "[Not Authenticated]"
    return response


#模拟用户登录
from flask import session,abort
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return "<h1>欢迎登录</h1>"

#模拟用户登出
from flask import  session
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('redirect_session'))




#重定向回上一个页面
#####################################################################

@app.route('/foo')
def foo():
    return '<h1>Foo Page</h1> <a href="%s">Do Something</a>' % url_for('do_something',next=request.full_path)

@app.route('/bar')
def bar():
    return '<h1>Bar Page</h1> <a href="%s">Do Something</a>' % url_for('do_something',next=request.full_path)#request.full_path是相对url,这里是"/bar?"

# @app.route('/do_something')
# def do_something():
#     return redirect(request.args.get('next',url_for('hello')))

"""
#在下面url安全验证中重写此函数
def redirect_back(default='hello',**kwargs):
    for target in request.args.get('next'),request.referrer:
        if target:
            return redirect(target)
        return redirect(url_for(default, **kwargs))
"""

@app.route('/do_something')
def do_something():
    return redirect_back()

#########################################################################

#对URL进行安全验证,判断url是否属于程序内部
from urllib.parse import urlparse,urljoin
from flask import request
def is_safe_url(target):
    ref_url=urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url,target))
    return test_url.scheme in ('http','https') and ref_url.netloc == test_url.netloc
#ruleparse()将URL分解为6个片段:scheme是协议，netloc是服务器地址，path是相对路径，params是参数，query是查询的条件。
#urljoin()将基地址和相对地址拼接

def redirect_back(default='hello',**kwargs):
    for target in request.args.get('next'),request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default,**kwargs))


#AJAX

from jinja2.utils import generate_lorem_ipsum
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data){
                $('.body').append(data);
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)







