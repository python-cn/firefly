from __future__ import absolute_import
# coding=utf-8

from flask_script import Manager, Server, Shell

from firefly.app import create_app

from firefly.models.user import Role, User, SocialConnection


def make_shell_context():
    return {
        "Role": Role,
        "User": User,
        "SocialConnection": SocialConnection
    }

manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', Server(
    use_debugger=True,
    use_reloader=True,
    host='0.0.0.0')
)

if __name__ == '__main__':
    manager.run()
