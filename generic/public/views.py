# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, url_for

# from flask_security import login_required, login_user, logout_user
from flask_login import login_required, login_user, logout_user

from generic.extensions import login_manager
from generic.public.forms import LoginForm
from generic.user.forms import RegisterForm
from generic.user.models import User
from generic.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/')  # , methods=['GET', 'POST'])
def home():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    """
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    """
    return render_template('public/home.html', form=form)


@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    """Log in."""
    # login_user()
    # flash('You are logged out.', 'info')
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash('You are logged in.', 'success')
            redirect_url = request.args.get('next') or url_for('user.members')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('public/login.html', form=form)
    # return redirect(url_for('public.login'))


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        User.create(username=form.username.data, email=form.email.data,
                    password=form.password.data, active=True)
        flash('Thank you for registering. You can now log in.', 'success')
        return redirect(url_for('public.login'))  # TODO auto-post to /login
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)


@blueprint.route('/find/')
def find():
    """Find item."""
    form = LoginForm(request.form)
    return render_template('public/find.html', form=form)


@blueprint.route('/item/')
def item():
    """item page."""
    form = LoginForm(request.form)
    return render_template('public/item.html', form=form)


@blueprint.route('/contact/')
def contact():
    """Contact info."""
    form = LoginForm(request.form)
    return render_template('public/contact.html', form=form)


@blueprint.route('/blog/')
def blog():
    """Blog page."""
    form = LoginForm(request.form)
    return render_template('public/blog.html', form=form)


@blueprint.route('/blog/post/1')
def post1():
    """Blog post page."""
    form = LoginForm(request.form)
    return render_template('public/blog-post-1.html', form=form)


@blueprint.route('/blog/post/2')
def post2():
    """Blog post page."""
    form = LoginForm(request.form)
    return render_template('public/blog-post-2.html', form=form)


@blueprint.route('/blog/post/3')
def post3():
    """Blog post page."""
    form = LoginForm(request.form)
    return render_template('public/blog-post-3.html', form=form)
