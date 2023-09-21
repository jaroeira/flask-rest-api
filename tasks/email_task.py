import requests
from app.utils import render_template
import os


def send_email(to, subject, body, html):

    email_api_url = os.environ.get('EMAIL_API_URL')
    email_domain = os.environ.get('EMAIL_DOMAIN')

    print(f"{email_api_url}/{email_domain}/messages")

    return requests.post(f"{email_api_url}/{email_domain}/messages",
          auth=("api", os.environ.get("EMAIL_API_KEY")),
          data={"from": f"Mailgun Sandbox <postmaster@{email_domain}>",
              "to": f"<{to}>",
              "subject": subject,
              "text": body,
              "html": html
              }
    )


def send_verification_email(email, username, verification_url):
    return send_email(
        email, 
        'Flask REST API - Verification E-Mail',
        'Please click on the link below to verify your email address',
         render_template('email/verify_email.html', username=username, verification_url=verification_url)
        )