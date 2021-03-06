#-*-coding:utf-8-*-
#-------------------------------------
# Name: 启动脚本
# Purpose: 
# Author:
# Date:
#-------------------------------------

#覆盖检测
import os
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')#启动覆盖检测引擎
    COV.start()

from app import create_app, db
from app.models import User, Role, Permission, Post
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
    

#定义shell上下文
def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Permission=Permission, Post=Post)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


#启动单元测试
@manager.command
def test(coverage=False):
    """Run the unit tests."""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        import sys
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:#覆盖检测
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()


#在请求分析器的监视下运行程序
@manager.command
def profile(length=25, profile_dir=None):
    """Start the application under the code profile."""
    from werkzeug.contrib.profiler import ProfilerMiddleware
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length],
                                        profile_dir=profile_dir)
    app.run()


#部署命令
@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from app.models import Role, User
    
    #把数据库迁移到最新修订版本
    upgrade()
    
    #创建用户角色
    Role.insert_roles()
    
    #让所有用户都关注此用户
    User.add_self_follows()
    
if __name__ == '__main__':
    manager.run()