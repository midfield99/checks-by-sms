import os
import sys
import unittest



class TestMain(unittest.TestCase):
    pass


#checks that the necessary environmental variables are set.
class TestEnv(unittest.TestCase):
        def test_checkbook_key(self):
            self.assertTrue(os.environ.get('CHECKBOOK_KEY'))
            self.assertNotEqual(os.environ.get('CHECKBOOK_KEY'), 'FAKE_KEY')

        def test_checkbook_secret(self):
            self.assertTrue(os.environ.get('CHECKBOOK_SECRET'))
            self.assertNotEqual(os.environ.get('CHECKBOOK_SECRET'), 'FAKE_SECRET')

        def test_checkbook_url(self):
            self.assertTrue(os.environ.get('CHECKBOOK_URL'))


if __name__ == '__main__':
    unittest.main()