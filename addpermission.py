from webapp.models import PermissionModel,RoleModel,role_permission,db
from webapp.extensions import permissions
from webapp import app

with app.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    # is while within this block. Therefore, you can now run........
    for permission in permissions:
        p = PermissionModel.query.filter_by(action=permission['action']).first()
        if not p:
            p = PermissionModel(
                name=permission['name'],
                action=permission['action']
            )
            db.session.add(p)
            db.session.commit()


    role = RoleModel.query.first()  # 获取第一条记录
    # 遍历那些没有删除的用户
    for p in PermissionModel.query.filter_by(is_delete=False):
        print('这句被执行')
        r = db.session.query(role_permission).join(RoleModel).join(PermissionModel).\
            filter(
                RoleModel.id == role.id,
                RoleModel.is_delete == False,
                PermissionModel.id == p.id,
                PermissionModel.is_delete == False,
                role_permission.c.is_delete == False,
            ).first()
        print('r=',r)
        if not r:
            # 添加role
            role.permissions.append(p)
    # role.save()