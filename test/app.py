import os
from flask import Flask,url_for,render_template,redirect,flash,abort
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy  
from wtforms import SubmitField,TextAreaField
from wtforms.validators import DataRequired

app = Flask(__name__)
db= SQLAlchemy(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','secret string')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL','sqlite:////'+os.path.join(app.root_path,'data.db'))
@app.route('/')
def index():
    return render_template('index.html')


class NewNoteForm(FlaskForm):
    body = TextAreaField('Body',validators=[DataRequired()])
    submit = SubmitField('Save')

class Note(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text)