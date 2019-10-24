from flask import Flask

app = Flask(__name__)

user = {
    'username' : '蔡徐坤',
    'bio' : '唱,跳,rap,篮球',
}

movies = [
    {'name':'My Neighbor Totore','year':'1983'},
    {'name':'Three Colours trilogy','year':'1993'},
    {'name':'Forrest Gump','year':'1994'},
    {'name':'Perfect Blue','year':'1997'},
]

from flask import render_template

@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html',user=user,movies=movies)

from flask import Flask,render_template

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'),404










