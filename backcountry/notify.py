# import sendgrid

# from sendgrid.helpers.mail import Mail, Email, To, Content

# my_sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

# # Change to your verified sender
# from_email = Email("your_email@example.com")

# # Change to your recipient
# to_email = To("destination@example.com")

# subject = "Lorem ipsum dolor sit amet"
# content = Content("text/plain", "consectetur adipiscing elit")

# mail = Mail(from_email, to_email, subject, content)

# # Get a JSON-ready representation of the Mail object
# mail_json = mail.get()

# # Send an HTTP POST request to /mail/send
# response = my_sg.client.mail.send.post(request_body=mail_json)

import os
import json
import sys

try:
    from dotenv import load_dotenv

    load_dotenv('.env')
except ModuleNotFoundError:
    pass

import smtplib
from email.mime.text import MIMEText


def make_message(email, text):
    return {
        "from_email": "sam@bookhead.net",
        "from_name": "Sam McAlilly",
        "subject": "Your campsite status alerts",
        "text": text,
        "to": [{"email": email, "type": "to"}],
    }


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()


# def send_email(message):
#     key = os.getenv('MAILCHIMP_API_KEY')
#     try:
#         mailchimp = MailchimpTransactional.Client(api_key=key)
#         response = mailchimp.messages.send({"message": message})
#     except ApiClientError as error:
#         print("An exception occurred: {}".format(error.text))


target_file = sys.argv[1]
with open(target_file) as f:
    notifications = json.load(f)

print('notifications', notifications)

if notifications:
    for email, subscription in notifications.items():
        sites = {}
        for site_name, dates in subscription.items():
            sites[site_name] = []
            for date, status in dates.items():
                sites[site_name].append((date, status['remaining']))

        text = f""

        for site_name, details in sites.items():
            for d in details:
                text += f"{site_name} has {d[1]} available for {d[0]}\n"

        text += "\nU better hurry up and book ur campsite. Visit https://www.recreation.gov/permits/4675321/registration/detailed-availability/ & grab that permit.\n\nO yea here is a map: https://www.nps.gov/glac/planyourvisit/upload/Wilderness-Campground-Map-2023.pdf\n\n"

        send_email(
            "Your tracked campsite(s) in Glacier changed",
            text,
            'smcalilly@gmail.com',
            [email],
            os.getenv('GMAIL_APP_PASSWORD'),
        )
        print('sent email to', email)
else:
    print('no notifications to send')
