import os
import sys
import unittest
from dotenv import load_dotenv

from Check import Check
from app import send_check

load_dotenv('.env')

class TestMain(unittest.TestCase):
    #test message parsing:
    #"Send ${amount} to {name} ({email}) for {description}"
    format_msg = 'Format is:Send ${amount} to {name} ({email}) for {description}'

    def test_valid_check(self):
        msg = "Send $5 to John Snow (john.snow@westeros.com) for The Night Watch"
        expected = {"name":'John Snow', "recipient":'john.snow@westeros.com', 
                    "amount": 5.0, "description": "The Night Watch"}
        c = Check(msg)
        self.assertEqual(c.checkbook_post_data(), expected)

    def test_invalid_check(self):
        msg = "send 5 to John Snow john.snow@westeros.com) for armor."
        expected = ['Start message with "Send"', 'Invalid amount.', 
                    'Invalid name', 'Invalid email', self.format_msg]
        c = Check(msg)
        
        self.assertTrue(c.errors)
        self.assertEqual(c.errors, expected)

    #test specific error messages
    def test_general_error(self):
        msg = "send $5 to John Snow (john.snow@westeros.com) for The Night Watch"
        expected = ['Start message with "Send"', self.format_msg]
        c = Check(msg)
        
        self.assertTrue(c.errors)
        self.assertEqual(c.errors, expected)

    def test_name_error(self):
        msg = "Send $5 toJohn Snow (john.snow@westeros.com) for The Night Watch"
        expected = ["Invalid name", self.format_msg]
        c = Check(msg)
        
        self.assertTrue(c.errors)
        self.assertEqual(c.errors, expected)

    def test_email_error(self):
        msg = "Send $5 to John Snow {0}{1}"
        no_rparen = Check(msg.format('(john.snow@westeros.com', ' for The Night Watch'))
        no_lparen = Check(msg.format('john.snow@westeros.com)', ' for The Night Watch'))
        valid_no_for1 = Check(msg.format('(john.snow@westeros.com)', None))
        valid_no_for2 = Check(msg.format('(john.snow@westeros.com).', None))
        valid_for = Check(msg.format('(john.snow@westeros.com)', ' for The Night Watch'))
        
        self.assertTrue(no_rparen.errors)
        self.assertEqual(no_rparen.errors, ["Invalid email", self.format_msg])

        self.assertTrue(no_lparen.errors)
        self.assertEqual(no_lparen.errors, ["Invalid name", "Invalid email", self.format_msg])

        self.assertFalse(valid_no_for1.errors)
        self.assertEqual(valid_no_for1.email, 'john.snow@westeros.com')

        self.assertFalse(valid_no_for2.errors)
        self.assertEqual(valid_no_for2.email, 'john.snow@westeros.com')

        self.assertFalse(valid_for.errors)
        self.assertEqual(valid_for.email, 'john.snow@westeros.com')


    def test_amount_error_general(self):
        msg = "Send 5 to John Snow (john.snow@westeros.com) for The Night Watch"
        expected = ['Invalid amount.', self.format_msg]
        c = Check(msg)
        
        self.assertTrue(c.errors)
        self.assertEqual(c.errors, expected)

    def test_amount_error_not_number(self):
        msg = "Send $five to John Snow (john.snow@westeros.com) for The Night Watch"
        expected = ['Amount is not a number.', self.format_msg]
        c = Check(msg)
        
        self.assertTrue(c.errors)
        self.assertEqual(c.errors, expected)

    def test_amount_error_is_number(self):
        msg = "Send {0} to John Snow (john.snow@westeros.com) for The Night Watch"
        expected = ['Amount can only have two decimal places.', self.format_msg]

        no_dec = Check(msg.format('$500'))
        extra_zeros = Check(msg.format('$5.20000'))
        frac = Check(msg.format('$5.123'))
        
        self.assertFalse(no_dec.errors)
        self.assertEqual(no_dec.amount, 500)

        self.assertFalse(extra_zeros.errors)
        self.assertEqual(extra_zeros.amount, 5.20)

        self.assertTrue(frac.errors)
        self.assertEqual(frac.errors, expected)
        self.assertEqual(frac.amount, None)


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
