#!/usr/bin/env python
from project.application import create_app
from project.config import DevelopmentConfig
from project.apps.auth.models import User, Role, Permission, Group
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand
from project.extensions import db
import urlparse



application = create_app(DevelopmentConfig)
manager = Manager(application)
migrate = Migrate(application, db)

def make_shell_context():
    return dict(application=application, db=db, User=User, Role=Role,
                Permission=Permission, Group=Group)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def deploy():
    """Run deployment tasks."""
    from flask.ext.migrate import upgrade
    from project.apps.auth.models import Role, User

    # migrate database to latest revision
    upgrade()

    # create user roles
    Role.insert_roles()


if __name__ == '__main__':
    manager.run()