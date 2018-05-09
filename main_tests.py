import os
import sys
import unittest



class TestMain(unittest.TestCase):
    pass


#checks that the necessary environmental variables are set.
class TestEnv(unittest.TestCase):
    #Checkbook.io setup.
    def test_checkbook_key(self):
        self.assertTrue(os.environ.get('CHECKBOOK_KEY'))
        self.assertNotEqual(os.environ.get('CHECKBOOK_KEY'), 'FAKE_KEY')

    def test_checkbook_secret(self):
        self.assertTrue(os.environ.get('CHECKBOOK_SECRET'))
        self.assertNotEqual(os.environ.get('CHECKBOOK_SECRET'), 'FAKE_SECRET')

    def test_checkbook_url(self):
        self.assertTrue(os.environ.get('CHECKBOOK_URL'))

    #Twilio setup.
    def test_twilio_sid(self):
        self.assertTrue(os.environ.get('TWILIO_ACCOUNT_SID'))
        self.assertNotEqual(os.environ.get('TWILIO_ACCOUNT_SID'), 'FAKE_SID')

    def test_twilio_auth(self):
        self.assertTrue(os.environ.get('TWILIO_AUTH_TOKEN'))
        self.assertNotEqual(os.environ.get('TWILIO_AUTH_TOKEN'), 'FAKE_TOKEN')


    def test_twilio_number(self):
        self.assertTrue(os.environ.get('TWILIO_NUMBER'))
        self.assertNotEqual(os.environ.get('TWILIO_NUMBER'), 'FAKE_NUMBER')


if __name__ == '__main__':
    unittest.main()