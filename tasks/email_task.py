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


def send_verification_email(email, username, verification_token):

    base_url = os.environ.get('BASE_URL')
    verification_url = f"{base_url}/auth/verify-email?token={verification_token}"

    return send_email(
        email,
        'Flask REST API - Verification E-Mail',
        'Please click on the link below to verify your email address',
        render_template('email/verify_email.html',
                        username=username, verification_url=verification_url)
    )


def send_password_reset_email(email, password_reset_token):
    base_url = os.environ.get('BASE_URL')
    password_reset_url = f"{base_url}/auth/reset-password?token={password_reset_token}"

    return send_email(
        email,
        'Flask REST API - Password Reset',
        'Please click on the link below to reset your password. The link will be valid for 24 hours.',
        render_template('email/reset_password.html',
                        password_reset_url=password_reset_url)
    )
