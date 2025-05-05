import os
import json
import datetime
import requests
from oauthlib.oauth2 import WebApplicationClient

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

from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest
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


class TravelEntry(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    destination = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    description = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()


client = WebApplicationClient(GOOGLE_CLIENT_ID)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('pages/home.html', current_user=current_user)
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

        new_user = User(username=username, email=email, password=password) # TODO: Hash password & email verify??
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

    if not db.session.get(User, userid):
        db.session.add(new_user)
        db.session.commit()

    login_user(new_user)
    return redirect(url_for("home"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/friends")
@login_required
def friends():
    return render_template('pages/friends.html', 
                           current_user=current_user, 
                           friends=[id_to_user(friend_id) for friend_id in get_friends_ids(current_user.id)],
                           pending=[id_to_user(req_id) for req_id in get_friends_request_ids(current_user.id)])


def get_friends_ids(uid):
    return [x.friend_id for x in FriendEntry.query.filter_by(user_id=uid, status='accepted')] + [x.user_id for x in FriendEntry.query.filter_by(friend_id=uid, status='accepted')]


def get_friends_request_ids(uid):
    return [x.user_id for x in FriendEntry.query.filter_by(friend_id=uid, status='pending')]


def id_to_user(uid):
    return db.session.get(User, uid)


@app.route("/friends/request", methods=['POST']) # form friend with complementary request / handle request acceptance and rejection
@login_required
def friends_request():
    email = request.form['email']

    user_query = User.query.filter_by(email=email).first()

    if not user_query:
        return "User not found", 400
    
    comp = FriendEntry.query.filter_by(user_id=user_query.id, friend_id=current_user.id).first() # Check for incoming complementary request
    if comp and comp.status == 'pending':
        comp.status = 'accepted'
        db.session.add(comp)
        db.session.commit()
        print("YAY FRIENDS")
        return redirect(url_for("friends"))


    if FriendEntry.query.filter_by(user_id=current_user.id, friend_id=user_query.id).first() or comp and comp.status == 'accepted': # Check repeat and fulfilled request
        return "Unable to request", 400

    new_entry = FriendEntry(
        user_id=current_user.id, friend_id=user_query.id, status="pending"
    )

    db.session.add(new_entry)
    db.session.commit()

    return redirect(url_for("friends"))


def get_travel_data(uid):
    return TravelEntry.query.filter_by(user_id=uid)


@app.route("/travels/<user_id>")
@login_required
def travel_profile(user_id):
    user_id = int(user_id)
    if user_id == current_user.id or user_id in get_friends_ids(current_user.id):
        return render_template('pages/travels.html', user=id_to_user(user_id), travel_data=get_travel_data(user_id))
    return "Not authorized", 404


@app.route("/travels", methods=['GET', 'POST'])
@login_required
def travels():
    if request.method == 'POST':
        destination = request.form['destination']
        date = [int(i) for i in request.form['date'].split('-')]
        date = datetime.date(date[0], date[1], date[2])
        description = request.form['description']

        travel_entry = TravelEntry(
            user_id=current_user.id, 
            destination=destination, 
            date=date, 
            description=description
        )

        db.session.add(travel_entry)
        db.session.commit()
        return redirect(url_for('travels'))

    return render_template('pages/travels.html', travel_data=get_travel_data(current_user.id))


if __name__ == '__main__':
    app.run(debug=True, ssl_context="adhoc")
