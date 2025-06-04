"""
class BrevoApiEmailBackend and helpers

This class implements an EmailBackend compatible with Django.
The primary goal is to use API based email for Django logging and
user notification.
For now, we only consider text contents, no attachments, no cc, bcc, reply_to
or header information.
"""
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMessage
from brevo_python import (TransactionalEmailsApi, ApiClient, Configuration,
                          SendSmtpEmail)
from brevo_python.rest import ApiException

class BrevoApiEmailBackend(BaseEmailBackend):

    def send_messages(self, email_messages):
        print("In BrevoApiEmailBackend.send_messages")
        configuration = configure()
        api_instance = TransactionalEmailsApi(ApiClient(configuration))

        success_count = 0
        for email_message in email_messages:
            email = convert_email_to_brevo(email_message)
            result = send(api_instance, email)
            if result:
                success_count += 1
        return success_count


def configure():
    # Configure API key authorization: api-key
    apikey = settings.BREVO_API_KEY
    configuration = Configuration()
    configuration.api_key['api-key'] = apikey
    configuration.api_key['partner-key'] = apikey
    return configuration

def convert_email_to_brevo(email_message):
    email = SendSmtpEmail()
    email.to = [{'email': addr} for addr in email_message.to]
    email.subject = email_message.subject
    email.sender = {'email': email_message.from_email}
    email.text_content = email_message.body
    return email
    
def send(api_instance, email):
    success = False
    try:
        api_response = api_instance.send_transac_email(email)
        print(api_response)
        success = True
    except ApiException as e:
        print("Exception when calling "
              "TransactionalEmailsApi->send_transac_email: %s\n" % e)
    return success
