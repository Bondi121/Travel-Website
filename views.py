from flask import Flask, render_template, request, redirect, url_for, flash
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+os.path.join(basedir, 'travel_db.sqlite')
db.init_app(app)
migrate = Migrate(app, db)

app.config['SECRET_KEY'] = 'DAFASDF ADSFASD'

class Contact(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class Newsletter(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String, nullable=False)
    

with app.app_context():
    db.create_all()


@app.route("/home")
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register" , methods=["POST", "GET"])
def register():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        check_email = User.query.filter_by(email=email).first()
        if check_email is None:
            if password == confirm_password:
                user = User(first_name=first_name, last_name=last_name, email=email, password=password)
                db.session.add(user)
                db.session.commit()
                flash("You have successfully created an account", "success")
            else:
                flash("Your password and your confirmed password have to be the same", "info")
                return redirect(url_for('register'))
        else:
            flash("Your email has already been used, please use another one", "info")
            return redirect (url_for('register'))
    return render_template("register.html")



@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/newsletter", methods=["POST", "GET"])
def newsletter():
    if request.method == "POST":
        subscriber_email = request.form['email']
        subscriber = Newsletter(email=subscriber_email)
        db.session.add(subscriber)
        db.session.commit()
        flash('You have successfully subscribed to the newsletter', 'success')
        return redirect(url_for('contact'))


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST": 
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        message = request.form['message']
        create_message = Contact(name=name,phone_number=phone_number, email=email, message=message)
        db.session.add(create_message)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("contact.html")


@app.route("/service")
def services():
    return render_template("services.html")



   # flask --app views.py --debug run
