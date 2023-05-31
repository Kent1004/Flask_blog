from flask import Blueprint, render_template
from flask_login import login_required
from werkzeug.exceptions import NotFound

from blog.app import login_manager
from blog.models import User

user = Blueprint('user', __name__, url_prefix='/users', static_folder='../static')


# USERS  = ['Alice','Jon','Mike']
# USERS = {
#     1: {"name": "Ivan"},
#     2: {"name": "Jon"},
#     3: {"name": "Mary"}
# }

@user.route('/')
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
    user = User.query.filter_by(id=pk).one_or_none()
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
