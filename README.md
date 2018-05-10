#checks-by-sms

##Introduction
This project connects the Twilio and Checkbook.io api to enable sending checks by text. Messages sent to the Twilio number will be parse, and a digital check will be sent via the Checkbook.io API.
A response will then be sent, including message errors if message parsing failed.
Valid format for messages: "Send ${amount} to {name} ({email}) for {description}"

##Setup
###Server
This application needs a server with a public IP address. Part of the application requires that Twilio call the server, so this can't be tested fully locally.
This was tested with an EC2 t2.micro instance.

clone this repo
Create a virtual environment:
`python3 -m venv checks-by-sms`
Activate it:
`source bin/activate`
Move into the directory:
`cd checks-by-sms`
Add credentials:
`cp env-sample.txt .env`
Add your checkbook.io credentials to .env. These are located here:
https://checkbook.io/account/settings/developer


Setup your Twilio account:
Note: Twilio will block messaging unverified phone numbers if you have trial account. This impacts functionality.
https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply-python#configure-your-webhook-url
The address for the webhook is:
http://{public IP address for webserver}/send_check

Run tests:
`python app_tests.py`
Install pip requirements:
`pip install -r requirements.txt`
Run the server:
`flask run --host=0.0.0.0 --port=80`
