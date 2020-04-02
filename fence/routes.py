import os
import secrets
import fence.postAndCommentModel as postAndCommentModel
from flask import render_template, url_for, flash, redirect, request
from fence import app, db, bcrypt
from fence.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm, SearchForm
from fence.userModel import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/feed")
def feed():
    try:
        posts = postAndCommentModel.getAllPosts()
        return render_template('feed.html', posts=posts)
    except Exception as exc:
        return render_template('microservice_unavailable.html')

@app.route("/comment/nested/<int:post_id>/<int:parent_comment_id>", methods=['GET', 'POST'])
def comment_on_comment(post_id, parent_comment_id):
    form = CommentForm()
    if form.validate_on_submit():
        postAndCommentModel.commentOnComment(post_id, parent_comment_id, current_user.id, form.content.data)
        flash('Comment posted!')
        return redirect(url_for('post', post_id=post_id))
    return render_template('write_comment.html', form=form, legend="New Comment")


@app.route("/post/comment/<int:post_id>", methods=['GET', 'POST'])
def comment_on_post(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        postAndCommentModel.commentOnPost(post_id, current_user.id, form.content.data)
        flash('Comment posted!')
        return redirect(url_for('post', post_id=post_id))
    return render_template('write_comment.html', form=form, legend="New Comment")


@app.route("/post/write", methods=['GET', 'POST'])
def write_post():
    form = PostForm()
    if form.validate_on_submit():
        postAndCommentModel.newPost(form.title.data, form.content.data, current_user.id)
        flash('Posted!')
        return redirect(url_for('feed'))
    return render_template('write_post.html', form=form, legend="New Post")

@app.route("/post/<int:post_id>")
def post(post_id):
    try:
        # get post from microservice and display it along with its comments and ability to comment more
        post = postAndCommentModel.getPost(post_id)
        comments = postAndCommentModel.getCommentsForPost(post_id)
        return render_template('post.html', post=post, comments=comments)
    except Exception as exc:
        return render_template('microservice_unavailable.html')

@app.route("/search/write", methods=['GET', 'POST'])
def write_search_query():
    form = SearchForm()
    if form.validate_on_submit():
        try:
            posts_matching_search = postAndCommentModel.search(form.search_string.data)
            return render_template('feed.html', posts=posts_matching_search)
        except Exception as exc:
            return render_template('microservice_unavailable.html')
    return render_template('write_search.html', form=form, legend="Search")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))
    registrationForm = RegistrationForm()
    if registrationForm.validate_on_submit():  # WTForms will ensure all validators pass, otherwise will show error message
        hashed_password = bcrypt.generate_password_hash(registrationForm.password.data).decode('utf-8')
        # store new user in the DB
        user = User(username=registrationForm.username.data,
                    password=hashed_password)  # store hashed verion of password
        db.session.add(user)
        db.session.commit()
        # whatever you flash will be displayed by the base template
        flash('Your account has been created. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=registrationForm)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('feed'))  # if user logged in already, take them to feed screen
    loginForm = LoginForm()
    if loginForm.validate_on_submit():  # WTForms will ensure all validators pass, otherwise will show error message
        user = User.query.filter_by(username=loginForm.username.data).first()
        if user and bcrypt.check_password_hash(user.password, loginForm.password.data):
            login_user(user)  # tell the flask_login to log in the user
            # if user had tried to go to a page that is only allowed when you're logged in, redirect them there after they log in
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('feed'))
        else:
            flash('Login Unsuccessful. Please check username and password')
    return render_template('login.html', form=loginForm)


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
        db.session.commit()
        flash('Your account has been updated!')
        return redirect(url_for('account'))
    elif request.method == 'GET':  # prepopulate the fields with current username
        accountForm.username.data = current_user.username
    return render_template('account.html', form=accountForm)
