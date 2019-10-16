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


from flask import Flask,make_response
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name',name)
    return response

from flask import request
@app.route('/get_cookie')