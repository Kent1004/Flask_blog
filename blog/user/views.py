from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user, login_user
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash

from blog.extensions import db


from blog.app import login_manager
from blog.models import User
from blog.forms.user import UserRegisterForm

user = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


# USERS  = ['Alice','Jon','Mike']
# USERS = {
#     1: {"name": "Ivan"},
#     2: {"name": "Jon"},
#     3: {"name": "Mary"}
# }

@user.route('/')
@login_required
def user_list():
    from blog.models import User
    users = User.query.all()
    return render_template(
        'users/list.html',
        users=users,
    )


# @user.route("/<int:pk>")
# def get_user(pk: int):
#     if pk in USERS:
#         user_raw = USERS[pk]
#     else:
#         raise NotFound("User id:{}, not found".format(pk))
#     return render_template(
#         "users/profile.html",
#         user_name=user_raw["name"]
#     )


@user.route('/<int:pk>')
@login_required
def profile(pk: int):
    from blog.models import User
    user: User = User.query.filter_by(id=pk).one_or_none()
    if not user:
        raise NotFound(f'No such user {pk}')
    return render_template(
        "users/profile.html",
        user=user,
    )


def get_user_name(pk: int):
    user = User.query.filter_by(id=pk).one_or_none()
    if user:
        return user.email
    else:
        return 'Anonimus'


@user.route('/register',methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('user.profile', pk=current_user.id))
    form = UserRegisterForm(request.form)
    errors = []
    if request.method == 'POST' and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append('email not uniq')
            return render_template('users/register.html',form=form)
        _user = User(
            email = form.email.data,
            first_name = form.first_name.data,
            last_name=form.last_name.data,
            password = generate_password_hash(form.password.data)
        )

        db.session.add(_user)
        db.session.commit()
        login_user(_user)
    return render_template('users/register.html', form = form , errors= errors)