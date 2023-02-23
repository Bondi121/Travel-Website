from flask import Blueprint, request, flash, url_for, redirect, render_template
from flask_login import login_user 
from .models import User
from app_folder.extensions import db

users = Blueprint("users",__name__, template_folder="templates")


@users.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(password):
            #if password == user.password:
            
            next_page = request.args.get("next")
            if login_user(user):
                if next_page:
                    flash("You have logged in successfully", "success")
                    return redirect (next_page)
                else:
                    flash("You have logged in successfully", "success")
                    return redirect (url_for('pages.home'))
            else:
                flash("Incorrect email or password", "warning")
        else:
            flash("No user found with this email", "warning")
    return render_template("login.html")

@users.route("/register" , methods=["POST", "GET"])
def register():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        check_email = User.query.filter_by(email=email).first()
        if check_email is None:
            print(1)
            if password == confirm_password:
                print(2)
                user = User(first_name=first_name, last_name=last_name, email=email, password=password)
                db.session.add(user)
                print(3)
                db.session.commit()
                flash("You have successfully created an account", "success")
            else:
                flash("Your password and your confirmed password have to be the same", "info")
                return redirect(url_for('users.register'))
        else:
            flash("Your email has already been used, please use another one", "info")
            return redirect (url_for('users.register'))
    return render_template("register.html")


@users.route("/forget_password", methods=["POST", "GET"])
def forget_password():
    if request.method == "POST":
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user is not None:
            pass
    return render_template("forget_password.html")


