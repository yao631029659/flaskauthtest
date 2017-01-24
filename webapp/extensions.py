from functools import wraps
from flask import g
from webapp.models import UserModel
permissions = list()
class PermissionDeniedException(RuntimeError):
    """Permission denied to the resource."""

class Permission(object):

    def __init__(self, module=None, action=None):
        self.module = module
        self.action = action

    # 定义self.check 用来检查有没有对应的action权限
    def check(self, module, func):
        # 如果用户没有登陆 返回假
        if not self.current_user:
            print('没有登陆')
            return False
        # 返回值格式化 返回的东西应该长这样__main__.func
        # 因为currrent_user是UserModel的对象，所以这里的check调用了类的方法 查询了数据库
        return self.current_user.check('{module}.{action}'.format(
            module=module,
            action=func
        ))
    # 拒绝访问 提供给下面的装饰器调用的
    def deny(self):
        return '失败'
        # return fail(4003, u'无权访问')

    # 让类拥有函数的方法 permission(func) 太伟大了 整个就是一个装饰器 这个装饰器的外层是一个__call__里面返回decorator
    def __call__(self, func):
        # 添加一些参数进来 permissons是一个列表 func.__module__一般等于__main__()     func.__name__一般返回被修饰函数的名字
        # permissions应该是长这样
        # action:__main__,new
        # name:'this is a method delete'
        # 并且将func.__doc__来作为权限中的name
        permissions.append({
            'action': '{}.{}'.format(func.__module__, func.__name__),
            'name': func.__doc__
        })
        @wraps(func)
        def decorator(*args, **kwargs):
            # 调用上面定义的check方法，检查有没有对应的权限
            if not self.check(func.__module__, func.__name__):
                # 三个参数__main__  user_info
                return self.deny()
            # 如果检验通过了,返回视图
            return func(*args, **kwargs)
        # 返回装饰器
        return decorator


    # 会在with语句下调用
    def __enter__(self):
        if not self.check(self.module, self.action):
            try:
                self.deny()
            except Exception as e:
                raise e
            else:
                raise PermissionDeniedException()

    # 会在退出with语句下调用
    def __exit(self):
        pass
    # 新增了一个属性current_user

    @property
    def current_user(self):
        # 调用全局的user
        return UserModel(id=g.user)
    print("permission=",permissions)
permission = Permission()