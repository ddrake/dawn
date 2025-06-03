from django.conf import settings
import brevo_python
from brevo_python.rest import ApiException

def configure():
    # Configure API key authorization: api-key
    apikey = settings.BREVO_API_KEY
    configuration = brevo_python.Configuration()
    configuration.api_key['api-key'] = apikey
    configuration.api_key['partner-key'] = apikey
    return configuration

def sendmail(to, subject, html=None, text=None, sender=None):
    """
    Either HTML or text must be specified for the body
    Sample usage: sendmail(joe@user.com, "Greeting", text="Hi Joe")
    """
    success = False
    if sender is None:
        sender = settings.DEFAULT_FROM_EMAIL

    configuration = configure()
    api_instance = brevo_python.TransactionalEmailsApi(
            brevo_python.ApiClient(configuration))

    email = brevo_python.SendSmtpEmail()
    email.to = [{'email': to}]
    email.subject = subject
    email.sender = {'email': sender}

    if html is not None:
        email.html_content = html
    elif text is not None:
        email.text_content = text
    else:
        raise ValueError("Either html or text must be specified")
    
    try:
        api_response = api_instance.send_transac_email(email)
        print(api_response)
        success = True
    except ApiException as e:
        print("Exception when calling "
              "TransactionalEmailsApi->send_transac_email: %s\n" % e)
    return success
