from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.Model.models import Affiliate
from config import Config


class TestConfig(Config):
    TESTING = True
    # since this is testing, i think this is okay
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = Affiliate(firstname='fn', lastname='ln1')
        u.set_password('covid')
        self.assertFalse(u.check_password('flu'))
        self.assertTrue(u.check_password('covid'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
