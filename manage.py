#!/usr/bin/env python
import os
from app import create_app, db
from app.models import Recipe
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand


app = create_app(os.getenv('COOKBOOK_CONFIG') or 'default')
manager = Manager(app)
# use Alembic to manage DB migrations
migrate = Migrate(app, db)


# convenience -- have app, db, and Recipe already imported
# when you do 'python cookbook.py shell'
def make_shell_context():
    return dict(app=app, db=db, Recipe=Recipe)


@manager.command
def test():
    '''Run the unit tests.'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
