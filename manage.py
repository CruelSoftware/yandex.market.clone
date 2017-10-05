import os

from app import create_app, db
from flask_script import Manager
from flask_migrate import MigrateCommand
from flask_alchemydumps import AlchemyDumpsCommand, AlchemyDumps

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
alchemydumps = AlchemyDumps(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('alchemydumps', AlchemyDumpsCommand)

if __name__ == '__main__':
    manager.run()