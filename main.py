import os
import requests
from twilio.rest import Client




def checkbook_test():
    post_data ={"name":"Widgets Inc.","recipient":"widgets@example.com", "amount": 123.00}
    auth = os.environ.get('CHECKBOOK_KEY') + ':' + os.environ.get('CHECKBOOK_SECRET')
    headers={'Authorization': auth}
    send_digital = os.environ.get('CHECKBOOK_URL') + '/v3/check/digital'
    return requests.post(send_digital, headers=headers, json=post_data).json()



def twilio_send_test():
    client = Client(os.environ.get('TWILIO_ACCOUNT_SID'), os.environ.get('TWILIO_AUTH_TOKEN'))
    twilio_number = os.environ.get('TWILIO_NUMBER')
    msg = "sms from twilio succesful"

    #remove test_num later
    message = client.messages.create(body=msg,from_=twilio_number,to=os.environ.get('TEST_NUM'))

    return message