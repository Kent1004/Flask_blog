from flask_combo_jsonapi import ResourceList, ResourceDetail

from blog.extensions import db
from blog.models import User
from blog.schemas import UserSchema
from blog.api.permissions.user import UserPermission


class UserList(ResourceList):
    schema = UserSchema
    data_layer = {
        'session': db.session,
        'model': User,
    }


class UserDetail(ResourceDetail):
    schema = UserSchema
    data_layer = {
        'session': db.session,
        'model': User,
        'permission_get': [UserPermission],
    }