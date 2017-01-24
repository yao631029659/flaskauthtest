from webapp.models import db,UserModel,RoleModel,PermissionModel,MenuModel,user_role,role_permission,role_menu
from flask_script import Manager,Server
from webapp import app
manager = Manager(app)
@manager.shell
def make_shell_context():
    return dict(app=app,db=db,UserModel=UserModel,RoleModel=RoleModel,PermissionModel=PermissionModel,MenuModel=MenuModel,user_role=user_role,role_permission=role_permission,role_menu=role_menu)
if __name__=="__main__":
    manager.run()