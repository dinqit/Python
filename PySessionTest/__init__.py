"""
In this small app we are testing the flask.sessions and the workings of flask_login
to implement it in another application.
We will try to utilize some new python libraries.
We will use Flask-Login, SQLAlchemy in conjunction with WTForms.
Together they should provide authentication, authorization and a secure
User management system which we could even extend to an API login.

@file_name = '__init__.py'
@version = 01
@date = 06 jan 2020
@author Giovanni Herdigein
"""
from flask import request, sessions, redirect
from flask import Flask,render_template,request,session,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form,StringField,SubmitField,validators
from flask_login import LoginManager,UserMixin,login_user
import os

# configuration options
login_manager   = LoginManager()# Loginmanager
DEBUG           = True
app             = Flask(__name__)
app.config.from_object(__name__)
app.config['SERVER_NAME']='localhost'
app.config['SERVER_HOST']= 'Localhost'
app.config['SERVER_PORT']= 80
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

# initializing the parts for use
db= SQLAlchemy(app)# database init
login_manager.init_app(app)# LoginManager init

# Creating the tables for the database
class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id      = db.Column(db.Integer,primary_key = True)
    name    = db.Column(db.String(45) ,nullable = False,unique = True)
    email   = db.Column(db.String(128),nullable = False,unique = True)
    password= db.Column(db.String(20),nullable = False)
    is_active = db.Column(db.Boolean )
    #checking users password
    def check_password(self,password):
        if password == self.password:
            return True
        return False
    def is_active(self):
        return False

    #returning an instance of the user as a string
    def _str(self):
        return '<User : email= %, name=%',format(self.email,self.name)

# The login form class according to wtforms
class LoginForm(Form):
    email       =StringField('Email',[validators.DataRequired(),validators.Length(max = 128)])
    password    = StringField('Password',[validators.DataRequired(),validators.Length(min = 8,max = 20)])
    submit      = SubmitField('Verstuur')

# The registration form class extends Login class
class RegisterForm(LoginForm):
    name        = StringField('User Name:',[validators.DataRequired(),validators.Length(min = 3,max = 45)])
    confirm     = StringField('Repeat Password',[validators.DataRequired(),validators.Length(min = 8,max = 20),
        validators.EqualTo('password', message = 'Passwords must match')])

# this method retrieves the user from database from session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# index route of our application
@app.route('/')
def index():
    """
    This method is the index of our app.
    We will use it to lead to the most inner
    of our application
    """
    return render_template('index.html',title="index")

@app.route('/login',methods = ['GET','POST'])
def login():
    login_form = LoginForm(request.form)
    if login_form.validate():
        user = User.query.filter_by(email = login_form.email.data).first()

        if user is None:
            flash('Uw email adres onbekend in ons systeem')
            return redirect(url_for('login'))
        else :
            passwd = login_form.password.data
            if user.check_password(passwd):
                login_user(user)
                flash('U bent ingelogd')
                return redirect(url_for('index'))
            else:
                flash("Uw email adres en wachtwoord komen niet overeen")
                return redirect(url_for('login'))
    return render_template('login.html',form = login_form)

@app.route('/register',methods=['GET','POST'])
def register():
    register_form = RegisterForm(request.form)
    return render_template('register.html',form=register_form)

@app.route('/logout')
def logout():
    pass

# Here is our main file where we'll start the application
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(port = 80)
