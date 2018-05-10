import os
import sys
import unittest

from Check import Check
from app import send_check

class TestMain(unittest.TestCase):
    #test message parsing:
    #"Send $5 to John Snow (john.snow@westeros.com) for The Night Watch"
    #"Send ${amount} to {name} ({email}) for {description}"
    def test_valid_check(self):
        msg = "Send $5 to John Snow (john.snow@westeros.com) for The Night Watch"
        expected = {"name":'John Snow', "recipient":'john.snow@westeros.com', 
                    "amount": 5.0, "description": "The Night Watch"}
        c = Check(msg)
        print(c.errors)
        self.assertEqual(c.checkbook_post_data(), expected)

    def test_invalid_check(self):
        msg = "send 5 to John Snow john.snow@westeros.com) for armor."
        expected = ['Start message with "Send"', 'Invalid amount.', 
                    'Invalid name', 'Invalid email', 
                    'Format is:Send ${amount} to {name} ({email}) for {description}']
        c = Check(msg)
        
        self.assertTrue(c.errors)
        self.assertEqual(c.errors, expected)

    #Note, need to mock api calls and responses. Unit tests shouldn't hit databases
    # def test_send_check(self):
    #     msg = "Send $5 to John Snow (john.snow@westeros.com) for The Night Watch"

    #     c = Check(msg)
    #     response = send_check(c)
    #     print(response)
    #     print(response.json())

    #     self.assertTrue(False)


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

if __name__ == '__main__':
    unittest.main()
