from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_required, login_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from blog.app import login_manager
from blog.forms.auth import UserAuthForm
from blog.models import User


auth = Blueprint('auth', __name__, static_folder='../static')


# @auth.route('/login_old', methods=['POST', 'GET'])
# def login():
#     if request.method == 'GET':
#         if current_user.is_authenticated:
#             return redirect(url_for('user.profile', pk= current_user.id))
#         return render_template(
#             'auth/login_old.html'
#         )
#
#     email = request.form.get('email')
#     password = request.form.get('password')
#     from blog.models import User
#     user = User.query.filter_by(email=email).first()
#     if not user or not check_password_hash(user.password, password):
#         flash('Check your login details')
#         return redirect(url_for('.login'))
#
#     login_user(user)
#     return redirect(url_for('user.profile', pk=user.id))

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.profile', pk=current_user.id))
    form = UserAuthForm(request.form)
    if request.method == 'POST':
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password,password):
            return render_template('auth/login.html', form=form, error='No valid credentials')
        else:
            login_user(user)
            return redirect(url_for('user.profile', pk=user.id))
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))
