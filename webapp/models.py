from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
from datetime import datetime

# 关系表
user_role = db.Table('user_role',  # 用户角色关联表
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('created_at', db.DateTime, default=datetime.now),
)

role_permission = db.Table('role_permission',  # 角色权限关联表
    db.Column('permission_id', db.Integer, db.ForeignKey('permission.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('created_at', db.DateTime, default=datetime.now),
)

role_menu = db.Table('role_menu',  # 用户菜单关联表
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
    db.Column('menu_id', db.Integer, db.ForeignKey('menu.id')),
    db.Column('created_at', db.DateTime, default=datetime.now),
    db.Column('is_delete', db.Boolean, default=False),
)


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    mobile = db.Column(db.String(11))
    name = db.Column(db.String(50))
    gender = db.Column(db.SmallInteger)  # 0 未知， 1 男 2 女
    roles = db.relationship(
        'RoleModel',
        secondary=user_role,
        backref=db.backref(
            'users',
            lazy='dynamic'
        )
    )

    @property
    def permissions(self):
        permissions = PermissionModel.query.join(role_permission).join(RoleModel).join(user_role).join(UserModel). \
            filter(
            UserModel.id == self.id
        )
        return permissions

    @property
    def menus(self):
        menus = MenuModel.query.join(role_menu).join(RoleModel).join(user_role).join(UserModel). \
            filter(
            UserModel.id == self.id
        ).order_by(MenuModel.type_, MenuModel.order).all()
        return menus

    # 传入action参数 看看有没有权限
    def check(self, action):
        print("action=",action)
        # action=__main__.user_info 这是一个样例
        permission = self.permissions.filter(PermissionModel.action == action).first()
        return bool(permission)

class RoleModel(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(20))

class PermissionModel(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.Integer(),primary_key=True)
    name = db.Column(db.String(50))
    action = db.Column(db.String(250), unique=True)

class MenuModel(db.Model):
    __tablename__ = 'menu'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    icon = db.Column(db.String(50))
    url = db.Column(db.String(250))
    order = db.Column(db.SmallInteger, default=0)
    bg_color = db.Column(db.String(50))



