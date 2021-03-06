import os
import requests
from dotenv import load_dotenv
from flask import Flask, request, redirect
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from Check import Check

load_dotenv('.env')
app = Flask(__name__)

@app.route("/send_check", methods=['POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    # Determine the right reply for this message
    if body:
        sms_check = Check(body)
        if not sms_check.errors:
            response = send_check(sms_check)
            if response.status_code == 201:
                resp.message("The check was sent.")
            else:
                print("Checkbook.io API response info:")
                print(body)
                print(response.text)
                print(sms_check.checkbook_post_data())
                print(response.status_code)
                resp.message("API call was not successful.")
        else:
            print("Message parsing errors:")
            print(sms_check.errors)
            resp.message("Check is not valid." + str(sms_check.errors))

    return str(resp)

@app.route("/ping", methods=['GET'])
def ping():
    return "pong"


def send_check(sms_check):
    if sms_check.errors:
        return None

    auth = str(os.environ.get('CHECKBOOK_KEY')) + ':' + str(os.environ.get('CHECKBOOK_SECRET'))
    headers={'Content-type':'application/json', 'Authorization': auth}
    send_digital = str(os.environ.get('CHECKBOOK_URL')) + '/v3/check/digital'

    return requests.post(send_digital, headers=headers, 
                        json=sms_check.checkbook_post_data())

if __name__ == "__main__":
    app.run(debug=True)
