"""
Email all active users (initially these will be pre-activated)

mpy shell
from hours.scripts import email_preset_users
email_preset_users.send_emails(is_test=True)
"""

from django.contrib.auth.models import User


def send_email(user):
    subject = "Instructions for logging in to DAWN volunteer hours app"

    body = f"""Hi {user.first_name},

For grant applications, it will be extremely helpful if you could begin to use the new DAWN Volunteer Hours application to fill in the hours you worked in 2024 (we hope you will continue to use it to fill in hours for future years).

To make this as simple as possible, we have pre-registered you by creating a profile with the username: {user.username} and the email address we have on file for you: {user.email}.  Here are the steps to get started:

1. Browse to the web location: dawnus.app, and choose your desired language (English or Ukrainian).  You should be on the login page.  Under the login form there is a link: "Need username or password".

2. Click the link "Need username or password".  You will be asked to fill in your email address.  Please fill in the email address we have on file for you, i.e. {user.email}.

3. Check your inbox (and junk email if needed) for an email from webmaster@dawnus.app and click the link in that email.  This should open a browser tab where you can set and confirm your password.  Once you have done so, you should be taken back to the login page.

4. Log in to the Hours app with your username: {user.username} and the password you just created.

5. At the top right, you should see "User: <your username>".  If you are a U.S. Citizen, please click that link to see your user profile, check the box for U.S. Citizen, and click "Update" to save.

6. Start to input your best estimates for the hours you worked in 2024.  Once we reach the new year, it will no longer be possible to add hours for 2024.

If you have any trouble using this app, please check for open issues at github.com/ddrake/dawn/issues and, if your issue hasn't been reported yet, click "New Issue" and let us know the details.

Thank you for your continued support!"""

    user.email_user(subject, body, from_email="webmaster@dawnus.app")


def send_emails(is_test=False):
    if is_test:
        user = User.objects.get(first_name='Dow')
        send_email(user)
    else:
        for user in User.objects.filter(is_active=True):
            send_email(user)
