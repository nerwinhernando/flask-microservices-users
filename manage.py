# manage.py


import unittest

from flask_script import Manager

from project import create_app, db
from project.api.models import User


app = create_app()
manager = Manager(app)

# 1. This registers a new command, recreate_db, to the manager so that we can run the it from the 
#  command line Apply the model to the dev database:
# $ docker-compose run users-service python manage.py recreate_db
# 2. hop into sql
# $ docker exec -ti $(docker ps -aqf "name=users-db") psql -U postgres
@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()

# $ docker-compose up -d --build
# $ docker-compose run users-service python manage.py test
@manager.command
def test():
    """Runs the tests without code coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
