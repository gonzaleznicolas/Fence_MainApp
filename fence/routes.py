import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from fence import app, db, bcrypt
from fence.forms import RegistrationForm, LoginForm, UpdateAccountForm
from fence.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/feed")
def feed():
    return render_template('feed.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    registrationForm = RegistrationForm()
    if form.validate_on_submit(): #WTForms will ensure all validators pass, otherwise will show error message
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # store new user in the DB
        user = User(username=form.username.data, email=form.email.data, password=hashed_password) #store hashed verion of password
        db.session.add(user)
        db.session.commit()
        # whatever you flash will be displayed by the base template
        flash('Your account has been created. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=registrationForm)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('feed')) # if user logged in already, take them to feed screen
    loginForm = LoginForm()
    if form.validate_on_submit(): #WTForms will ensure all validators pass, otherwise will show error message
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user) #tell the flask_login to log in the user
            # if user had tried to go to a page that is only allowed when you're logged in, redirect them there after they log in
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('feed'))
        else:
            flash('Login Unsuccessful. Please check email and password')
    return render_template('login.html', title='Login', form=loginForm)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('feed'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('account'))
    elif request.method == 'GET': # prepopulate the fields with current username and email
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)