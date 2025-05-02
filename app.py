import os
import json

from flask import Flask, redirect, request, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
    UserMixin,
)
from oauthlib.oauth2 import WebApplicationClient
from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = os.environ.get("SECRET_KEY")

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=True)


class FriendEntry(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    friend_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    status = db.Column(db.String(10), nullable=False)  # 'pending', 'accepted', 'rejected'


with app.app_context():
    db.create_all()


client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('pages/home.html', username=current_user.username)
    return redirect(url_for('login'))


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            return "Email already exists", 400

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('home'))
    return render_template('pages/register.html')


@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user_query = User.query.filter_by(email=email).first()

        if not user_query:
            return "No such email", 400
        
        if user_query.password != password:
            return "Wrong password", 400

        login_user(user_query)

        return redirect(url_for('home'))
    return render_template("pages/login.html")


@app.route("/login/callback", methods = ['GET', 'POST'])
def gl_callback():    
    try:
        idinfo = id_token.verify_oauth2_token(request.form['credential'], GoogleRequest(), GOOGLE_CLIENT_ID)

        userid = int(idinfo['sub']) % (2**(8*2)) # TODO: Maybe do somethin about this
    except ValueError:
        return "Invalid token", 400

    new_user = User(
        id=userid, username=idinfo['name'], email=idinfo['email'], password=None
    )

    email_query = User.query.filter_by(email=idinfo['email']).first()
    if email_query:
        login_user(email_query)
        return redirect(url_for("home"))

    if not User.query.get(userid):
        db.session.add(new_user)
        db.session.commit()

    login_user(new_user)
    return redirect(url_for("home"))


@app.route("/logout") # TODO: This ain't working lol
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


app.run(debug=True, ssl_context="adhoc")
