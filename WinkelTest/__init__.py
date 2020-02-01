# init.py
# @_author "Giovanni Herdigein"
# @_version 0.1
# ---------------------

from flask import Flask, render_template,request,flash,redirect,session,jsonify
from wtforms import Form,StringField,validators,SubmitField,PasswordField
from flask_sqlalchemy import SQLAlchemy
# app configuration
DEBUG=True
app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"]='secret'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

db= SQLAlchemy(app)

# class represents a User from the database
class User(db.Model):
    id          = db.Column(db.Integer,primary_key=True)
    username    = db.Column(db.String(45),nullable=False)
    email       = db.Column(db.String(45),nullable=False)
    password    = db.Column(db.String(8),nullable=False)

# this class will be rendered into a login form
class LoginForm(Form):
    name = StringField('Name:')
    email = StringField('Email:', validators=[validators.Length(min=6, max=35)])
    password = PasswordField('Password:', validators=[validators.Length(min=3, max=35)])
    submit = SubmitField("Submit")

# First route of the application
@app.route('/')
def index():
    title = "Index"
    return render_template("index.html", title=title)

# This route leads to the login form
@app.route('/auth/login')
def login():
    loginform = LoginForm()
    return render_template('auth/login.html',form = loginform)

@app.route('/auth/authorize',methods=['POST'])
def authorize():

    if request.form['email']=='':
        flash('You should enter an email address')
        loginform = LoginForm()
        return render_template('auth/login.html', form=loginform)
    elif request.form['password']=='':
        flash('You did not enter a password')
        loginform = LoginForm()
        return render_template('auth/login.html', form=loginform)
    else:
        email = request.form['email']
        password = request.form['password']
        user  = User.query.filter_by(email=email).filter_by(password=password).first()
        if user:
            session['user_id']= user.id
            usr = {
                'id',user.id,
                'name',user.name,
                'email',user.email,
            }
            return redirect('index.html',usr=usr)
        else:
            return redirect('index.html')

# running the app from here
if __name__ == "__main__":
    app.run(port=80)
