import os
import secrets
from flask import render_template, url_for, flash, redirect, request
from fence import app, db, bcrypt
from fence.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm
from fence.models import User
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        "id": "0",
        "author": "Joe Jackson",
        "title": "What is software?",
        "content": "Soeone explain it to me...",
        "comments": [
            {"id": "1", "level": 0, "user": "Jack", "content": "Ah"},
            {"id": "2", "level": 1, "user": "Charlie", "content": "What"},
            {"id": "3", "level": 2, "user": "Alice", "content": "Ok"},
            {"id": "4", "level": 2, "user": "Bob", "content": "lol"}
        ]
    },
    {
        "id": "1",
        "author": "Steve Terry",
        "title": "What is fence",
        "content": "What is this website?",
        "comments": []
    },
    {
        "id": "2",
        "author": "Mike Lund",
        "title": "I like software",
        "content": "Do you all agree?",
        "comments": [
            {"id": "1", "level": 0, "user": "Jared", "content": "love it!"},
            {"id": "3", "level": 1, "user": "keemstar", "content": "love you!"},
            {"id": "2", "level": 0, "user": "Jared", "content": "love it XD!"}
        ]
    }
]


@app.route("/")
@app.route("/feed")
def feed():
    return render_template('feed.html', posts=posts)


@app.route("/comment/<int:post_id>", methods=['GET', 'POST'])
def comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        flash('Posted the following: %s' % form.content.data)
        flash('Posted!')
        return redirect(url_for('feed'))
    return render_template('write_post.html', title='New Comment', form=form, legend="New Comment")


@app.route("/post/write", methods=['GET', 'POST'])
def write_post():
    form = PostForm()
    if form.validate_on_submit():
        # tell the model about the post. form.title.data, form.content.data, user, time
        flash('Posted the following: %s: %s' % (form.title.data, form.content.data))
        flash('Posted!')
        return redirect(url_for('feed'))
    return render_template('write_post.html', title='New Post', form=form, legend="New Post")

@app.route("/post/<int:post_id>")
def post(post_id):
    # get post from microservice and display it along with its comments and ability to comment more
    post = posts[post_id]
    return render_template('post.html', post=post)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    registrationForm = RegistrationForm()
    if registrationForm.validate_on_submit():  # WTForms will ensure all validators pass, otherwise will show error message
        hashed_password = bcrypt.generate_password_hash(registrationForm.password.data).decode('utf-8')
        # store new user in the DB
        user = User(username=registrationForm.username.data, email=registrationForm.email.data,
                    password=hashed_password)  # store hashed verion of password
        db.session.add(user)
        db.session.commit()
        # whatever you flash will be displayed by the base template
        flash('Your account has been created. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=registrationForm)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))  # if user logged in already, take them to feed screen
    loginForm = LoginForm()
    if loginForm.validate_on_submit():  # WTForms will ensure all validators pass, otherwise will show error message
        user = User.query.filter_by(email=loginForm.email.data).first()
        if user and bcrypt.check_password_hash(user.password, loginForm.password.data):
            login_user(user)  # tell the flask_login to log in the user
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
    accountForm = UpdateAccountForm()
    if accountForm.validate_on_submit():
        current_user.username = accountForm.username.data
        current_user.email = accountForm.email.data
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('account'))
    elif request.method == 'GET':  # prepopulate the fields with current username and email
        accountForm.username.data = current_user.username
        accountForm.email.data = current_user.email
    return render_template('account.html', title='Account', form=accountForm)
