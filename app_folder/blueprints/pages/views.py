from flask import Blueprint, request, flash, url_for, redirect, render_template

from .models import Contact, Newsletter
from app_folder.extensions import db

pages = Blueprint("pages",__name__, template_folder="templates")


@pages.route("/home")
@pages.route("/")
def home():
    return render_template("index.html")


@pages.route("/about")
def about():
    return render_template("about.html")

@pages.route("/blog")
def blog():
    return render_template("blog.html")


@pages.route("/newsletter", methods=["POST", "GET"])
def newsletter():
    if request.method == "POST":
        subscriber_email = request.form['email']
        subscriber = Newsletter(email=subscriber_email)
        db.session.add(subscriber)
        db.session.commit()
        flash('You have successfully subscribed to the newsletter', 'success')
        return redirect(url_for('pages.contact'))


@pages.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST": 
        name = request.form['name']
        phone_number = request.form['phone_number']
        email = request.form['email']
        message = request.form['message']
        create_message = Contact(name=name,phone_number=phone_number, email=email, message=message)
        db.session.add(create_message)
        db.session.commit()
        return redirect(url_for('pages.home'))
    return render_template("contact.html")


@pages.route("/service")
def services():
    return render_template("services.html")

